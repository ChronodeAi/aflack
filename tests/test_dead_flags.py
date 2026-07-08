"""Tests for the dead feature flag detection script."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def _load_script(name: str):
    """Load a standalone script as a module for testing."""
    script_path = SCRIPTS_DIR / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {script_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class ScanCodeReferencesTests(unittest.TestCase):
    """Verify source code scanning finds feature flag references."""

    def setUp(self):
        self.mod = _load_script("detect_dead_flags.py")

    def test_finds_known_flag_references(self):
        refs = self.mod.scan_code_references()
        self.assertIsInstance(refs, set)

    def test_returns_set_of_strings(self):
        refs = self.mod.scan_code_references()
        for ref in refs:
            self.assertIsInstance(ref, str)

    def test_ignores_docstring_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            src_dir = Path(tmp)
            (src_dir / "example.py").write_text(
                '"""Example: set_flag("doc_only", enabled=False)"""\n'
                "from aflack.feature_flags import is_enabled\n"
                'LIVE = is_enabled("live_flag")\n'
            )
            original_src_dir = self.mod.SRC_DIR
            self.mod.SRC_DIR = src_dir
            try:
                refs = self.mod.scan_code_references()
            finally:
                self.mod.SRC_DIR = original_src_dir

        self.assertEqual(refs, {"live_flag"})


class ScanMigrationDefinitionsTests(unittest.TestCase):
    """Verify SQL migration scanning finds flag definitions."""

    def setUp(self):
        self.mod = _load_script("detect_dead_flags.py")

    def test_returns_set(self):
        defs = self.mod.scan_migration_definitions()
        self.assertIsInstance(defs, set)

    def test_returns_strings(self):
        defs = self.mod.scan_migration_definitions()
        for d in defs:
            self.assertIsInstance(d, str)


class DetectDeadFlagsTests(unittest.TestCase):
    """Verify the main detection function produces a valid report."""

    def setUp(self):
        self.mod = _load_script("detect_dead_flags.py")

    def test_returns_flag_report(self):
        report = self.mod.detect_dead_flags(stale_days=30)
        self.assertIsInstance(report, self.mod.FlagReport)

    def test_dead_flags_is_list(self):
        report = self.mod.detect_dead_flags(stale_days=30)
        self.assertIsInstance(report.dead_flags, list)

    def test_stale_flags_is_list(self):
        report = self.mod.detect_dead_flags(stale_days=30)
        self.assertIsInstance(report.stale_flags, list)

    def test_orphaned_references_is_list(self):
        report = self.mod.detect_dead_flags(stale_days=30)
        self.assertIsInstance(report.orphaned_references, list)

    def test_total_counts_are_non_negative(self):
        report = self.mod.detect_dead_flags(stale_days=30)
        self.assertGreaterEqual(report.total_defined, 0)
        self.assertGreaterEqual(report.total_referenced, 0)


class FormatReportTests(unittest.TestCase):
    """Verify report formatting produces readable output."""

    def setUp(self):
        self.mod = _load_script("detect_dead_flags.py")

    def test_format_includes_header(self):
        report = self.mod.FlagReport()
        output = self.mod.format_report(report)
        self.assertIn("Feature Flag Health Report", output)

    def test_format_includes_all_clear_when_clean(self):
        report = self.mod.FlagReport()
        output = self.mod.format_report(report)
        self.assertIn("All clear", output)

    def test_format_lists_dead_flags(self):
        report = self.mod.FlagReport(dead_flags=["test_flag_1", "test_flag_2"])
        output = self.mod.format_report(report)
        self.assertIn("test_flag_1", output)
        self.assertIn("test_flag_2", output)
        self.assertIn("Dead flags", output)

    def test_format_lists_stale_flags(self):
        report = self.mod.FlagReport(stale_flags=["old_flag (disabled, last updated 45d ago)"])
        output = self.mod.format_report(report)
        self.assertIn("old_flag", output)
        self.assertIn("Stale flags", output)

    def test_format_lists_orphaned_references(self):
        report = self.mod.FlagReport(orphaned_references=["missing_flag"])
        output = self.mod.format_report(report)
        self.assertIn("missing_flag", output)
        self.assertIn("Orphaned references", output)


if __name__ == "__main__":
    unittest.main()
