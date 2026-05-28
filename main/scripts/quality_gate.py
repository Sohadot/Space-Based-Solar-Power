#!/usr/bin/env python3
"""Quality Gate — aggregates all validators and blocks the build on any failure."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "main" / "scripts"

VALIDATORS = [
    "validate_schema.py",
    "validate_content.py",
    "validate_links.py",
    "validate_sources.py",
    "validate_claims.py",
    "validate_seo.py",
    "validate_sitemap.py",
    "validate_internal_link_graph.py",
    "validate_output_integrity.py",
    "validate_decision_log.py",
    "validate_glossary.py",
    "validate_questions.py",
]


def run_validator(script_name: str) -> tuple[str, int, str]:
    script_path = SCRIPTS_DIR / script_name
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    return script_name, result.returncode, result.stdout + result.stderr


def main() -> int:
    print("QUALITY GATE REPORT")
    print("=" * 50)
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Root: {ROOT}")
    print()

    results = []
    total_failures = 0

    for validator in VALIDATORS:
        name, code, output = run_validator(validator)
        status = "PASS" if code == 0 else "FAIL"
        if code != 0:
            total_failures += 1
        results.append((name, status, output))
        print(f"  [{status}] {name}")
        if code != 0:
            for line in output.strip().splitlines():
                print(f"         {line}")

    print()
    print(f"Total validators: {len(VALIDATORS)}")
    print(f"Failures: {total_failures}")

    if total_failures > 0:
        print()
        print("Build: BLOCKED")
        print("Fix all validation errors before deploying.")
        return 1

    print()
    print("Build: APPROVED")
    print("All validators passed. Public output is approved for deployment.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
