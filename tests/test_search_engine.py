"""Smoke tests for the BM25 search engine, domain detection, and the
design-system generator. Guards the runtime that every platform install ships.
"""
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "src" / "ui-ux-pro-max" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import core  # noqa: E402
import design_system  # noqa: E402

DOMAIN_QUERIES = {
    "style": "glassmorphism dashboard",
    "color": "fintech color palette",
    "chart": "compare categories bar chart",
    "landing": "saas landing page hero",
    "product": "beauty spa booking",
    "ux": "touch target accessibility",
    "typography": "elegant serif luxury",
    "icons": "arrow navigation icon",
    "react": "memo rerender optimization",
    "web": "form input aria",
    "google-fonts": "geometric sans",
}


@pytest.mark.parametrize("domain", sorted(core.CSV_CONFIG), ids=str)
def test_every_domain_returns_results(domain):
    result = core.search(DOMAIN_QUERIES[domain], domain=domain)
    assert "error" not in result, result
    assert result["domain"] == domain
    assert result["count"] > 0, f"no results for {domain}"
    for row in result["results"]:
        assert row, f"empty result row in {domain}"


@pytest.mark.parametrize("stack", core.AVAILABLE_STACKS, ids=str)
def test_every_stack_returns_results(stack):
    result = core.search_stack("performance", stack)
    assert "error" not in result, result
    assert result["count"] > 0, f"no results for stack {stack}"


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("color palette for a bank", "color"),
        ("bar chart of revenue", "chart"),
        ("landing page hero section", "landing"),
        ("glassmorphism style", "style"),
        ("react rerender memo", "react"),
        ("lucide icon set", "icons"),
        ("no keyword overlap whatsoever", "style"),  # fallback default
    ],
)
def test_detect_domain(query, expected):
    assert core.detect_domain(query) == expected


def test_regression_bauhaus_geometric_pairing_searchable():
    # This pairing was destroyed by a fused CSV row; keep it findable.
    result = core.search("bauhaus geometric", domain="typography")
    names = [r.get("Font Pairing Name") for r in result["results"]]
    assert "Bauhaus Geometric" in names, names


def test_regression_neo_brutalism_mobile_complete():
    # This row's checklist and design variables were truncated by a stray quote.
    result = core.search("neo brutalism mobile", domain="style")
    row = next(
        r for r in result["results"] if r["Style Category"] == "Neo Brutalism (Mobile)"
    )
    assert row["Design System Variables"].startswith("--bg:")
    assert "avoided" in row["Implementation Checklist"]


def test_bm25_ranks_matching_doc_first():
    bm25 = core.BM25()
    bm25.fit(["red green blue", "typography fonts pairing", "charts and graphs"])
    ranked = bm25.score("typography pairing")
    assert ranked[0][0] == 1
    assert ranked[0][1] > 0


def test_design_system_generation_and_persistence(tmp_path):
    out = design_system.generate_design_system(
        "saas analytics dashboard",
        project_name="Smoke Test",
        output_format="markdown",
        persist=True,
        page="dashboard",
        output_dir=str(tmp_path),
    )
    assert "Smoke Test" in out
    masters = list(tmp_path.glob("design-system/*/MASTER.md"))
    assert masters, "MASTER.md was not persisted"
    overrides = list(tmp_path.glob("design-system/*/pages/dashboard.md"))
    assert overrides, "page override was not persisted"
