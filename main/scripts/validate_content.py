#!/usr/bin/env python3
"""Content Validator — blocks thin content, placeholders, and AI filler."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "main" / "content" / "pages"
DATA_DIR = ROOT / "main" / "data"

ERRORS = []

# Patterns that indicate actual placeholder/filler content.
# Deliberately specific: governance text that discusses these anti-patterns
# (e.g. "no placeholder titles") must not trigger false positives.
PLACEHOLDER_PATTERNS = [
    r"lorem ipsum",
    r"coming soon",
    r"\bTODO\b",
    r"\[placeholder\]",          # bracket-wrapped placeholder
    r"placeholder content",      # explicit filler label
    r"placeholder text",         # explicit filler label
    r"\[insert content here\]",
    r"\bTBD\b",
    r"content pending",
    r"under construction",
    r"\[add content\]",
    r"\[fake article\]",         # bracket-wrapped fake article token
    r"sample text",
    r"\[your \w+ here\]",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in PLACEHOLDER_PATTERNS]


def error(msg: str):
    ERRORS.append(msg)
    print(f"  [FAIL] {msg}")


def load_json(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        error(f"{path.name}: JSON parse error: {e}")
        return None


def extract_text(obj, parts=None) -> str:
    if parts is None:
        parts = []
    if isinstance(obj, str):
        parts.append(obj)
    elif isinstance(obj, list):
        for item in obj:
            extract_text(item, parts)
    elif isinstance(obj, dict):
        for v in obj.values():
            extract_text(v, parts)
    return " ".join(parts)


def check_placeholders(text: str, file_name: str):
    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            error(f"{file_name}: placeholder pattern '{pattern.pattern}' detected")


def check_minimum_length(text: str, file_name: str, min_len: int = 200):
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) < min_len:
        error(f"{file_name}: content too short ({len(clean)} chars, minimum {min_len})")


def check_duplicate_paragraphs(text: str, file_name: str):
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 80]
    seen = set()
    for para in paragraphs:
        if para in seen:
            snippet = para[:60]
            error(f"{file_name}: duplicate paragraph detected: '{snippet}...'")
        seen.add(para)


def validate_page_content_files():
    if not CONTENT_DIR.exists():
        return
    for json_file in CONTENT_DIR.glob("*.json"):
        data = load_json(json_file)
        if not data:
            continue
        text = extract_text(data)
        check_placeholders(text, json_file.name)
        check_minimum_length(text, json_file.name, min_len=300)
        check_duplicate_paragraphs(text, json_file.name)


def validate_generated_glossary():
    path = DATA_DIR / "glossary_terms.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    terms = data if isinstance(data, list) else data.get("terms", [])
    for term in terms:
        tid = term.get("id", "<no-id>")
        definition = term.get("definition", "")
        check_placeholders(definition, f"glossary/{tid}")
        if len(definition.strip()) < 100:
            error(f"glossary/{tid}: definition under 100 chars")


def main() -> int:
    print("validate_content.py")
    print("-" * 40)
    validate_page_content_files()
    validate_generated_glossary()
    if ERRORS:
        print(f"\nContent validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Content validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
