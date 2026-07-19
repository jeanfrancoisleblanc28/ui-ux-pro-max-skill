# OPERATIONAL DIAGNOSTIC — RAPID SPRINT
**Repo:** `ui-ux-pro-max-skill` · **Date:** 2026-07-19 · **Method:** 10-minute evidence-first sweep (manifests → CI → data integrity → distribution pipeline)
**Scope:** high-friction workflows, data anomalies, single-point-of-failure processes. Every finding below was **reproduced live**, not inferred.

---

## ⛔ FINDING 1 — BROKEN SOURCE-OF-TRUTH: EVERY FRESH INSTALL SHIPS PARTIALLY-CHINESE INSTRUCTIONS

| | |
|---|---|
| **Severity** | ⛔ **CRITICAL** — user-facing on all ~18 supported platforms |
| **Class** | Single-point-of-failure workflow (manual SKILL.md regeneration) |
| **Status** | ✅ VERIFIED — rendered templates and diffed against shipped artifact |

**Evidence.** Commit `87c6c3e` ("fix(skills): translate Chinese to English") patched only the **generated** file `.claude/skills/ui-ux-pro-max/SKILL.md` — the exact file CLAUDE.md forbids hand-editing. The **source templates** it renders from were never fixed:

- `src/ui-ux-pro-max/templates/base/quick-reference.md` — **23 lines of untranslated Chinese**
- `src/ui-ux-pro-max/templates/base/skill-content.md` — **7 lines of untranslated Chinese** (lines 38–41, 260–263) + stale stats (claims "67 styles" vs. the repo's published "50+")
- Render-vs-shipped diff: **13 divergent hunks** across a 654-line body

**Impact.** `npx uipro-cli init` renders SKILL/workflow files **from the templates** for every platform (claude, cursor, windsurf, copilot, …). Every fresh install since `87c6c3e` ships the untranslated, stale version — while the repo's own dogfooded copy looks clean, **masking the defect from the maintainer**. This is the textbook failure mode of the manual regeneration workflow ("run init in a scratch dir and copy the result back"): fixes land on one side of the pipe and silently never propagate.

**Relief (≈ half day, permanent):**
1. Port `87c6c3e`'s translation into `quick-reference.md` + `skill-content.md`; refresh the stats.
2. Regenerate `.claude/skills/ui-ux-pro-max/SKILL.md` from the fixed templates.
3. Add a **render-parity step** to `cli-sync-check.yml`: render the claude platform from templates, diff against the checked-in SKILL.md, fail on drift. (The workflow already guards asset mirroring and version alignment — this is the one missing leg.)

---

## 🟥 FINDING 2 — SILENT DATA CORRUPTION IN THE KNOWLEDGE BASES

| | |
|---|---|
| **Severity** | 🟥 **HIGH** — the product's core asset (search corpus) is quietly lossy |
| **Class** | Database anomaly (malformed rows, dead payload) |
| **Status** | ✅ VERIFIED — corruption reproduced through the live search engine |

**Evidence.** `csv.DictReader` shunts overflow fields into a discarded restkey and fills missing fields with `None`, so malformed rows **never error — they silently truncate**:

| File | Row | Anomaly | What users lose |
|---|---|---|---|
| `typography.csv` | No 57 "Gen Z Brutal" | 21 fields vs 11 — **two pairings fused into one row** | The entire **"Bauhaus Geometric" (Outfit)** pairing is unsearchable. Reproduced: `search.py "bauhaus geometric" --domain typography` returns *Geometric Modern* instead. |
| `styles.csv` | No 77 "Neo Brutalism (Mobile)" | 31 fields vs 22 (unescaped quote) | 9 fields dropped, incl. half the implementation checklist and the **entire Design System Variables** token set |
| `stacks/laravel.csv` | No 24, No 45 | 11 fields vs 10 | Docs URLs (Tailwind content-config, Laravel response headers) dropped |
| `stacks/angular.csv` | No 28 | 9 fields vs 10 | `Docs URL` = `None` |
| `stacks/astro.csv` | No 35 | 9 fields vs 10 | `Docs URL` = `None` |

**Bonus anomaly:** `data/design.csv` + `data/draft.csv` (near-duplicates, 208 KB ≈ **12% of the entire data payload**) are not valid CSV, are referenced by **zero code paths** (not in `CSV_CONFIG`), yet are synced into `cli/assets/` and copied into every install of every platform.

**Impact.** The product's value proposition *is* this data. Corruption is invisible at query time — output formats cleanly while entries vanish — so no user report will ever pinpoint it.

**Relief (≈ half day, closes the whole defect class):**
1. Repair the 6 malformed rows; resurrect "Bauhaus Geometric" as its own row.
2. Delete (or relocate out of `data/`) `design.csv` / `draft.csv`.
3. Add a ~30-line CSV schema validator (header uniqueness + exact field count per row) to CI. It would have caught **all five** files.

---

## 🟧 FINDING 3 — ZERO TEST COVERAGE ON THE ENGINE + STALE CI CONTRACT

| | |
|---|---|
| **Severity** | 🟧 **HIGH** — every regression ships blind to 18 platforms |
| **Class** | High-friction / absent verification workflow |
| **Status** | ✅ VERIFIED — workflow inspected, test discovery run repo-wide |

**Evidence.**
- CLAUDE.md documents CI as "**flake8 + pytest**". The actual workflow (`python-package-conda.yml`) runs **flake8 only**, restricted to syntax-error selectors (`E9,F63,F7,F82`). No pytest step exists.
- Repo-wide discovery finds **zero tests** for the core engine (`core.py` BM25 + `detect_domain`, `search.py`, `design_system.py` aggregation/persistence). The only `test_*.py` files belong to the sibling `ui-styling` skill and are never executed by CI.
- Consequence already realized: nothing gated the Finding-2 corruption or the Finding-1 drift into `main`.

**Impact.** The Python engine is the single runtime every one of the 18 platform installs executes. Any behavioral regression (tokenizer, ranking, domain detection, persistence paths) reaches all users with **no automated tripwire**, and the documented CI contract gives false confidence.

**Relief (≈ 1 day):**
1. Smoke suite: one search per domain (11) + per stack (16) asserts non-empty, well-formed results; a `detect_domain` table test; one end-to-end `--design-system --persist` run against a tmp dir.
2. Wire `pytest` into the workflow — honoring the contract CLAUDE.md already promises.
3. Fold in the Finding-2 CSV validator as a test so data and code share one gate.

---

## EXECUTION ORDER (ASYMMETRIC YIELD)

| # | Action | Effort | Yield |
|---|---|---|---|
| 1 | Fix templates + regenerate SKILL.md + render-parity CI | ~0.5 d | Un-ships broken content on every future install; kills the SPOF workflow |
| 2 | Repair 6 rows + drop 208 KB dead payload + CSV validator in CI | ~0.5 d | Restores lost knowledge; permanently closes the silent-corruption class |
| 3 | Pytest smoke suite + wire into CI | ~1 d | Converts the engine from unguarded to gated; makes docs honest |

**Total: ~2 days of work converts three standing, invisible failure modes into permanently guarded pipelines.**
