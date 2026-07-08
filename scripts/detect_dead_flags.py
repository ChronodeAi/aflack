#!/usr/bin/env python3
"""Detect dead and stale feature flags.

Scans the source code for feature flag references (is_enabled, get_flag,
set_flag calls) and compares them against flags defined in the database.
Reports:
  1. Dead flags: defined in the database but never referenced in source code.
  2. Stale flags: disabled flags that haven't been updated in N days.
  3. Orphaned references: flag names used in code but not defined in the database.

Works with or without a database connection. Without a database, it scans
SQL migration files for flag definitions and only reports orphaned references.

Usage:
    python scripts/detect_dead_flags.py [--stale-days 30] [--json report.json]

Exit codes:
    0 - No dead or stale flags found
    1 - Dead or stale flags detected
    2 - Script error (could not run)
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
MIGRATIONS_DIR = REPO_ROOT / "db" / "migrations"

# Patterns to find flag definitions in migration files.
FLAG_FUNCTION_NAMES = {"is_enabled", "get_flag", "set_flag"}


@dataclass
class FlagReport:
    dead_flags: list[str] = field(default_factory=list)
    stale_flags: list[str] = field(default_factory=list)
    orphaned_references: list[str] = field(default_factory=list)
    db_connected: bool = False
    total_defined: int = 0
    total_referenced: int = 0


def scan_code_references() -> set[str]:
    """Scan Python AST call sites for feature flag name references.

    AST scanning intentionally ignores comments, docstrings, and examples in
    prose. A previous regex implementation treated docstring examples such as
    ``set_flag("my_flag", ...)`` as live source references, creating false
    orphaned-reference reports during workspace health sweeps.
    """
    referenced: set[str] = set()
    for py_file in SRC_DIR.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name):
                function_name = func.id
            elif isinstance(func, ast.Attribute):
                function_name = func.attr
            else:
                continue
            if function_name not in FLAG_FUNCTION_NAMES or not node.args:
                continue
            first_arg = node.args[0]
            if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
                referenced.add(first_arg.value)
    return referenced


def scan_migration_definitions() -> set[str]:
    """Scan SQL migration files for flag name definitions (INSERT statements)."""
    defined: set[str] = set()
    if not MIGRATIONS_DIR.exists():
        return defined
    insert_re = re.compile(
        r"""INSERT\s+INTO\s+feature_flags\s*.*?VALUES\s*\(?\s*["']([^"']+)["']""",
        re.IGNORECASE | re.DOTALL,
    )
    for sql_file in MIGRATIONS_DIR.rglob("*.sql"):
        content = sql_file.read_text()
        for match in insert_re.finditer(content):
            defined.add(match.group(1))
    return defined


def query_db_flags() -> dict[str, dict] | None:
    """Query the database for all feature flags. Returns None if DB unavailable."""
    try:
        sys.path.insert(0, str(REPO_ROOT / "src"))
        from aflack.db import connect  # noqa: PLC0415

        flags: dict[str, dict] = {}
        with connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT name, enabled, rollout_percentage, description, updated_at FROM feature_flags")
            for row in cur.fetchall():
                flags[row[0]] = {
                    "enabled": row[1],
                    "rollout_percentage": row[2],
                    "description": row[3],
                    "updated_at": row[4],
                }
        return flags
    except Exception:
        return None


def detect_dead_flags(stale_days: int = 30) -> FlagReport:
    """Detect dead, stale, and orphaned feature flags."""
    report = FlagReport()
    code_refs = scan_code_references()
    report.total_referenced = len(code_refs)

    db_flags = query_db_flags()
    if db_flags is not None:
        report.db_connected = True
        report.total_defined = len(db_flags)
        db_flag_names = set(db_flags.keys())

        # Dead flags: in DB but not referenced in code
        report.dead_flags = sorted(db_flag_names - code_refs)

        # Stale flags: disabled and not updated in stale_days
        now = datetime.now(UTC)
        for name, info in db_flags.items():
            if not info["enabled"] and info["updated_at"]:
                age = (now - info["updated_at"]).days
                if age >= stale_days:
                    report.stale_flags.append(f"{name} (disabled, last updated {age}d ago)")
        report.stale_flags.sort()

        # Orphaned references: used in code but not defined in DB
        report.orphaned_references = sorted(code_refs - db_flag_names)
    else:
        # Fallback: use migration definitions
        migration_defs = scan_migration_definitions()
        report.total_defined = len(migration_defs)

        # Dead flags: in migrations but not referenced in code
        report.dead_flags = sorted(migration_defs - code_refs)

        # Orphaned references: used in code but not in migrations
        report.orphaned_references = sorted(code_refs - migration_defs)

    return report


def format_report(report: FlagReport) -> str:
    """Format the report as human-readable text."""
    lines = [
        "Feature Flag Health Report",
        "=" * 40,
        f"Database connected: {'yes' if report.db_connected else 'no (using migration scan)'}",
        f"Flags defined: {report.total_defined}",
        f"Flags referenced in code: {report.total_referenced}",
        "",
    ]

    if report.dead_flags:
        lines.append(f"Dead flags ({len(report.dead_flags)}):")
        for flag in report.dead_flags:
            lines.append(f"  - {flag}")
        lines.append("")

    if report.stale_flags:
        lines.append(f"Stale flags ({len(report.stale_flags)}):")
        for flag in report.stale_flags:
            lines.append(f"  - {flag}")
        lines.append("")

    if report.orphaned_references:
        lines.append(f"Orphaned references ({len(report.orphaned_references)}):")
        for ref in report.orphaned_references:
            lines.append(f"  - {ref}")
        lines.append("")

    if not report.dead_flags and not report.stale_flags and not report.orphaned_references:
        lines.append("All clear: no dead, stale, or orphaned flags detected.")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect dead and stale feature flags")
    parser.add_argument("--stale-days", type=int, default=30, help="Days before a disabled flag is considered stale")
    parser.add_argument("--json", metavar="PATH", help="Save JSON report to file")
    args = parser.parse_args()

    report = detect_dead_flags(stale_days=args.stale_days)
    output = format_report(report)
    print(output)

    if args.json:
        output_path = Path(args.json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(asdict(report), indent=2))
        print(f"\nJSON report saved to {output_path}")

    # Exit with error if dead or stale flags found
    has_issues = bool(report.dead_flags or report.stale_flags)
    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
