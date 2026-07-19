"""Structural validation of the CSV knowledge bases and rendered templates.

Every CSV must parse with a unique, non-empty header and every row must have
exactly as many fields as the header. csv.DictReader silently drops overflow
fields and None-fills missing ones, so malformed rows corrupt search output
without ever raising an error — this suite is the only gate.
"""
import csv
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "src" / "ui-ux-pro-max" / "data"
TEMPLATES = REPO / "src" / "ui-ux-pro-max" / "templates"

ALL_CSVS = sorted(DATA.glob("*.csv")) + sorted((DATA / "stacks").glob("*.csv"))

STACK_COLUMNS = [
    "No", "Category", "Guideline", "Description", "Do", "Don't",
    "Code Good", "Code Bad", "Severity", "Docs URL",
]


@pytest.mark.parametrize("path", ALL_CSVS, ids=lambda p: str(p.relative_to(DATA)))
def test_csv_structure(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows, f"{path.name} is empty"
    header = rows[0]
    assert all(h.strip() for h in header), f"{path.name}: blank header column"
    assert len(set(header)) == len(header), f"{path.name}: duplicate header columns"
    bad = [(i, len(r)) for i, r in enumerate(rows[1:], start=2) if len(r) != len(header)]
    assert not bad, (
        f"{path.name}: rows with wrong field count (expected {len(header)}): {bad[:5]}"
    )
    assert len(rows) > 1, f"{path.name}: no data rows"


@pytest.mark.parametrize(
    "path", sorted((DATA / "stacks").glob("*.csv")), ids=lambda p: p.stem
)
def test_stack_csv_columns(path):
    with open(path, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == STACK_COLUMNS, f"{path.name}: header deviates from stack schema"


CJK = re.compile(r"[　-〿一-鿿＀-￯]")

TRANSLATED_FILES = [
    TEMPLATES / "base" / "skill-content.md",
    TEMPLATES / "base" / "quick-reference.md",
    REPO / ".claude" / "skills" / "ui-ux-pro-max" / "SKILL.md",
] + sorted((TEMPLATES / "platforms").glob("*.json"))


@pytest.mark.parametrize("path", TRANSLATED_FILES, ids=lambda p: p.name)
def test_no_untranslated_cjk(path):
    hits = [
        (i, line[:80])
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if CJK.search(line)
    ]
    assert not hits, f"{path.name}: CJK text remains at {hits[:5]}"
