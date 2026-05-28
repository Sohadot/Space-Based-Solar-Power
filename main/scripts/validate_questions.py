#!/usr/bin/env python3
"""Questions Data Quality Validator — Sprint v1B-B.

Validates all questions with status 'approved' or 'approved_for_launch':
- Question has a substantive answer (non-empty, non-placeholder)
- Question has an answerBoundary
- Question has ≥2 relatedQuestions
- Question has ≥2 pageLinks
- No duplicate IDs or slugs
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK_PATH = ROOT / "main" / "data" / "question_bank.json"

PUBLISH_STATUSES = {"approved", "approved_for_launch"}
PLACEHOLDER_MARKERS = [
    "placeholder",
    "todo",
    "tbd",
    "lorem ipsum",
    "insert answer",
    "answer here",
]


def load_questions() -> list[dict]:
    with open(BANK_PATH, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get("questions", [])


def is_placeholder(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in PLACEHOLDER_MARKERS)


def validate_questions(questions: list[dict]) -> list[str]:
    errors = []
    seen_ids: dict[str, str] = {}
    seen_slugs: dict[str, str] = {}

    for q in questions:
        status = q.get("status", "")
        if status not in PUBLISH_STATUSES:
            continue

        qid = q.get("id", "")
        slug = q.get("slug", "")
        text = q.get("question", qid)

        # Duplicate ID check
        if qid in seen_ids:
            errors.append(f"Duplicate question ID '{qid}' (also '{seen_ids[qid]}')")
        else:
            seen_ids[qid] = text[:60]

        # Duplicate slug check
        if slug and slug in seen_slugs:
            errors.append(f"Duplicate slug '{slug}' (IDs: '{qid}' and '{seen_slugs[slug]}')")
        elif slug:
            seen_slugs[slug] = qid

        # Answer check
        answer = q.get("answer", "").strip()
        if not answer:
            errors.append(f"[{qid}] Missing answer")
        elif is_placeholder(answer):
            errors.append(f"[{qid}] Answer appears to be placeholder text")
        elif len(answer) < 100:
            errors.append(f"[{qid}] Answer too short ({len(answer)} chars); minimum substantive answer required")

        # answerBoundary check
        boundary = q.get("answerBoundary", "").strip()
        if not boundary:
            errors.append(f"[{qid}] Missing answerBoundary")
        elif is_placeholder(boundary):
            errors.append(f"[{qid}] answerBoundary appears to be placeholder text")

        # relatedQuestions check (≥2)
        related = q.get("relatedQuestions", [])
        if len(related) < 2:
            errors.append(f"[{qid}] Fewer than 2 relatedQuestions (has {len(related)})")

        # pageLinks check (≥2)
        page_links = q.get("pageLinks", [])
        if len(page_links) < 2:
            errors.append(f"[{qid}] Fewer than 2 pageLinks (has {len(page_links)})")

    return errors


def main() -> int:
    if not BANK_PATH.exists():
        print(f"ERROR: question_bank.json not found at {BANK_PATH}")
        return 1

    questions = load_questions()
    publish_questions = [q for q in questions if q.get("status", "") in PUBLISH_STATUSES]

    errors = validate_questions(questions)

    print("Questions Quality Report")
    print(f"  Total questions loaded:    {len(questions)}")
    print(f"  Publication-eligible:      {len(publish_questions)}")

    if errors:
        print()
        for err in errors:
            print(f"ERROR: {err}")
        print()
        print(f"Questions validation: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Questions validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
