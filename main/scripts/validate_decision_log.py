#!/usr/bin/env python3
"""Decision Log Integrity Validator — Sprint 2B.

DECISION_LOG is append-only. This validator fails if any decision ID
present in the base (main branch) DECISION_LOG is missing from the
current branch's DECISION_LOG.

Rule: new decisions may be added. Existing decisions must never be removed.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISION_LOG = ROOT / "DECISION_LOG"

ID_PATTERN = re.compile(r"\[([A-Z0-9]+-DL-[0-9]+)\]")

REQUIRED_IDS = [
    "S1-DL-010",
    "S1-DL-014",
    "S2-DL-001",
]


def extract_ids(text: str) -> set[str]:
    return set(ID_PATTERN.findall(text))


def get_base_ids() -> set[str]:
    """Read decision IDs from the main branch DECISION_LOG via git."""
    for ref in ("main", "origin/main"):
        try:
            result = subprocess.run(
                ["git", "show", f"{ref}:DECISION_LOG"],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            if result.returncode == 0 and result.stdout.strip():
                return extract_ids(result.stdout)
        except Exception:
            pass
    return set()


def main() -> int:
    if not DECISION_LOG.exists():
        print("ERROR: DECISION_LOG file not found")
        return 1

    current_text = DECISION_LOG.read_text(encoding="utf-8")
    current_ids = extract_ids(current_text)
    base_ids = get_base_ids()

    print("Decision Log Integrity")
    print(f"  IDs in base (main): {sorted(base_ids) if base_ids else '(could not read — skipping diff check)'}")
    print(f"  IDs in current:     {sorted(current_ids)}")

    errors = []

    # Check append-only rule against base
    if base_ids:
        missing_from_current = base_ids - current_ids
        if missing_from_current:
            errors.append(
                "Append-only rule violated — the following IDs were removed:\n    "
                + "\n    ".join(sorted(missing_from_current))
            )

    # Check hard-coded required IDs always exist
    for rid in REQUIRED_IDS:
        if rid not in current_ids:
            errors.append(f"Required decision ID [{rid}] is missing from DECISION_LOG")

    if errors:
        print()
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print()
    print("Decision log: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
