"""Tests for the build performance tracking script."""

from __future__ import annotations

import importlib.util
import sys
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


class StepResultTests(unittest.TestCase):
    """Verify StepResult dataclass behavior."""

    def setUp(self):
        self.mod = _load_script("track_build_performance.py")

    def test_creation_with_required_fields(self):
        result = self.mod.StepResult(
            name="test step",
            duration_seconds=1.5,
            success=True,
            command="echo hello",
        )
        self.assertEqual(result.name, "test step")
        self.assertEqual(result.duration_seconds, 1.5)
        self.assertTrue(result.success)
        self.assertEqual(result.command, "echo hello")


class BuildReportTests(unittest.TestCase):
    """Verify BuildReport dataclass behavior."""

    def setUp(self):
        self.mod = _load_script("track_build_performance.py")

    def test_starts_empty(self):
        report = self.mod.BuildReport()
        self.assertEqual(report.total_duration_seconds, 0.0)
        self.assertEqual(len(report.steps), 0)

    def test_add_accumulates_duration(self):
        report = self.mod.BuildReport()
        report.add(self.mod.StepResult("step1", 2.0, True, "cmd1"))
        self.assertEqual(report.total_duration_seconds, 2.0)
        report.add(self.mod.StepResult("step2", 3.0, True, "cmd2"))
        self.assertEqual(report.total_duration_seconds, 5.0)
        self.assertEqual(len(report.steps), 2)


class FormatGithubSummaryTests(unittest.TestCase):
    """Verify GitHub Actions summary formatting."""

    def setUp(self):
        self.mod = _load_script("track_build_performance.py")

    def test_includes_header(self):
        report = self.mod.BuildReport()
        output = self.mod.format_github_summary(report)
        self.assertIn("Build Performance Report", output)

    def test_includes_table_header(self):
        report = self.mod.BuildReport()
        output = self.mod.format_github_summary(report)
        self.assertIn("| Step | Duration (s) | Status |", output)

    def test_includes_step_data(self):
        report = self.mod.BuildReport()
        report.add(self.mod.StepResult("Lint", 1.2, True, "ruff check"))
        report.add(self.mod.StepResult("Tests", 5.4, False, "pytest"))
        output = self.mod.format_github_summary(report)
        self.assertIn("Lint", output)
        self.assertIn("1.2", output)
        self.assertIn("Tests", output)
        self.assertIn("5.4", output)
        self.assertIn("FAIL", output)
        self.assertIn("pass", output)

    def test_includes_total_time(self):
        report = self.mod.BuildReport()
        report.add(self.mod.StepResult("step1", 2.0, True, "cmd1"))
        report.add(self.mod.StepResult("step2", 3.0, True, "cmd2"))
        output = self.mod.format_github_summary(report)
        self.assertIn("5.0", output)

    def test_includes_cache_status(self):
        report = self.mod.BuildReport(cache_enabled=True)
        output = self.mod.format_github_summary(report)
        self.assertIn("yes", output)


if __name__ == "__main__":
    unittest.main()
