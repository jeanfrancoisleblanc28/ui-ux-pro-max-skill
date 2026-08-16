# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI/UX Pro Max is an AI design-intelligence toolkit distributed as a skill / workflow for AI coding assistants (Claude Code, Cursor, Windsurf, Copilot, Droid/Factory, Codex, Gemini, Kiro, Roo Code, Qoder, Trae, OpenCode, Continue, CodeBuddy, KiloCode, Warp, Augment, Antigravity).

It ships:

- A **Python search engine** (`src/ui-ux-pro-max/scripts/`) that runs offline with no external dependencies — BM25 + regex over CSV knowledge bases for styles, color palettes, typography, charts, UX guidelines, icons, and per-stack best practices.
- A **design-system generator** that aggregates multiple searches and applies reasoning rules from `ui-reasoning.csv` to recommend a complete design system (pattern + style + colors + typography + effects + anti-patterns).
- An **npm CLI (`uipro-cli`)** in `cli/` that installs the skill into any of ~18 supported AI assistants by rendering platform-specific templates and copying the data + scripts into the right folder (`.claude/`, `.cursor/`, `.windsurf/`, `.factory/`, `.codex/`, …).
- A **Claude marketplace plugin** packaged via `.claude-plugin/`.
- A **DÉPS AI Operating System** (`src/deps-ai-os/`) — a second, independent Python engine (also stdlib-only) that routes financing, valuation and economic-development work through 22 documented modules in 6 domains and enforces a quality gate before delivery. It is *not* part of the npm package; see the dedicated section below.

## Search Command

```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" [--domain <domain>] [--stack <stack>] [-n <max_results>] [--json]
```

If `--domain` is omitted, the script auto-detects the best domain from the query (see `detect_domain` in `core.py`).

**Domain search** (`--domain`, from `CSV_CONFIG` in `scripts/core.py`):

| Domain | CSV file | Purpose |
|---|---|---|
| `product` | `products.csv` | Product-type recommendations (SaaS, e-commerce, fintech, beauty, …) |
| `style` | `styles.csv` | UI styles (glassmorphism, minimalism, brutalism, …) with AI prompt + CSS keywords |
| `color` | `colors.csv` | 16-token color palettes by product type |
| `typography` | `typography.csv` | Font pairings with Google Fonts imports + Tailwind config |
| `google-fonts` | `google-fonts.csv` | Full Google Fonts catalog search |
| `chart` | `charts.csv` | Chart types, library recommendations, accessibility notes |
| `landing` | `landing.csv` | Landing-page patterns and CTA strategies |
| `ux` | `ux-guidelines.csv` | Cross-platform UX best practices + anti-patterns |
| `icons` | `icons.csv` | Icon libraries, names, import code |
| `react` | `react-performance.csv` | React/Next.js performance rules |
| `web` | `app-interface.csv` | Web app interface rules (ARIA, focus, forms, …) |

**Stack search** (`--stack`):

```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>
```

Available stacks (16, from `STACK_CONFIG` in `scripts/core.py`): `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `astro`, `nuxtjs`, `nuxt-ui`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`, `threejs`, `angular`, `laravel`.

**Design system generation** (`--design-system` / `-ds`):

```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --design-system [-p "Project Name"] [--format ascii|markdown]
```

Runs parallel searches across `product`, `style`, `color`, `landing`, `typography`, applies reasoning rules, and outputs a single recommended design system.

**Persist (Master + Overrides pattern):**

```bash
# Global source of truth
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"

# Plus a page-specific override
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

Writes to `design-system/<project-slug>/MASTER.md` and optionally `design-system/<project-slug>/pages/<page>.md`. Page overrides take precedence over the master at lookup time.

## DÉPS AI Operating System

A second engine, independent of the design search engine, living in `src/deps-ai-os/` and surfaced as the in-repo skill `.claude/skills/deps-ai-os/`. Its purpose is process enforcement, not design: it decides *which analysis modules run in which order* for a financing, valuation or economic-development request, and it blocks delivery of a deliverable that has not passed its controls.

```bash
python3 src/deps-ai-os/scripts/deps.py <commande> [options] [--json]
```

| Commande | Rôle |
|---|---|
| `route "<demande>"` | Oriente une demande en langage naturel vers un parcours ou un module, et signale les paramètres de politique non validés que la séquence mobilise |
| `module <ID\|nom>` | Fiche complète d'un module : entrées, méthode en étapes, sorties, pièges, formules, portes QA, chaîne d'exécution |
| `pipeline [<ID\|nom>]` | Liste les 8 parcours pré-câblés, ou détaille l'un d'eux |
| `params [--fonds] [--statut] [--module]` | Paramètres de la politique d'investissement et leur statut de validation |
| `formule [<recherche>] [--module]` | Les 24 formules normalisées avec termes, interprétation, seuils indicatifs et pièges |
| `qa [--module] [--bloquants]` | Les 28 contrôles qualité |
| `preflight [--type <CODE>]` | Liste à cocher avant remise, avec la convention de nommage attendue |
| `nomenclature [--type] [--module]` | Conventions de nommage et de versionnage des livrables |
| `doctor` | Contrôle d'intégrité du référentiel ; sort en code 1 si une anomalie est détectée |

**Structure : 22 modules en 6 domaines** — `01-FINANCEMENT` (F1–F4), `02-FLI-FLS` (P1–P4), `03-EVALUATION` (E1–E4), `04-DEVELOPPEMENT-ECONOMIQUE` (D1–D3), `05-PRODUCTION` (R1–R3, dont `R1 ui-ux-pro-max` qui fait le pont vers le moteur de design de ce dépôt), `06-QA` (Q1–Q4).

**Invariant central.** Les 22 paramètres de politique de `data/parametres-politique.csv` sont livrés au statut `A_VALIDER` avec la valeur `À_RENSEIGNER`. Le système ne connaît pas la politique d'investissement de l'organisation et n'invente aucune valeur : plafonds, taux, ratios entre fonds, mises de fonds minimales et seuils de délégation doivent être renseignés depuis le document en vigueur avant tout usage réel. Un test (`test_aucun_parametre_non_valide_ne_porte_de_valeur_chiffree`) empêche qu'une valeur inventée soit introduite dans un paramètre non validé.

Chaque domaine porte sa doctrine dans `src/deps-ai-os/references/<NN>-<domaine>.md`. Les seuils financiers d'usage (ratio de couverture, levier, etc.) vivent dans `formules.csv` et sont explicitement qualifiés d'`INDICATIF`, jamais de règle de politique.

## Architecture

```
src/ui-ux-pro-max/                  # Source of truth
├── data/                           # Canonical CSV knowledge bases
│   ├── products.csv, styles.csv, colors.csv, typography.csv,
│   ├── charts.csv, landing.csv, ux-guidelines.csv, icons.csv,
│   ├── google-fonts.csv, ui-reasoning.csv, react-performance.csv,
│   ├── app-interface.csv
│   ├── _sync_all.py                # Helper to keep colors.csv aligned with products.csv
│   └── stacks/                     # Per-stack guideline CSVs (16 files)
├── scripts/
│   ├── search.py                   # CLI entry point (argparse, formatting)
│   ├── core.py                     # BM25 engine + CSV_CONFIG + STACK_CONFIG + detect_domain
│   └── design_system.py            # Multi-domain aggregator + reasoning + persistence
└── templates/
    ├── base/
    │   ├── skill-content.md        # Common SKILL.md body (with {{TITLE}}, {{SCRIPT_PATH}}, …)
    │   └── quick-reference.md      # Extra section appended for platforms that want it
    └── platforms/                  # One JSON per platform: claude.json, cursor.json,
                                    # windsurf.json, agent.json (antigravity), copilot.json,
                                    # kiro.json, roocode.json, codex.json, qoder.json,
                                    # gemini.json, trae.json, opencode.json, continue.json,
                                    # codebuddy.json, droid.json, kilocode.json, warp.json,
                                    # augment.json

cli/                                # npm package `uipro-cli` (v2.5.0)
├── src/
│   ├── index.ts                    # Commander entry point
│   ├── commands/
│   │   ├── init.ts                 # Renders templates + copies data/scripts into project
│   │   ├── update.ts               # Re-runs init to refresh
│   │   ├── uninstall.ts            # Removes platform folders (see AI_FOLDERS)
│   │   └── versions.ts             # Lists available versions
│   ├── utils/
│   │   ├── template.ts             # Reads platforms/*.json + base templates, renders SKILL files
│   │   ├── detect.ts               # Auto-detects which assistant is in use
│   │   ├── extract.ts              # Legacy ZIP-based install
│   │   ├── github.ts               # GitHub release fetching (legacy path)
│   │   └── logger.ts
│   └── types/index.ts              # AIType, AI_FOLDERS, PlatformConfig
├── assets/                         # Generated mirror of src/ui-ux-pro-max/{data,scripts,
│                                   #   templates} — gitignored, regenerated by `npm run sync`
│                                   #   (also auto-runs on `npm install` and before pack/publish)
├── scripts/
│   ├── sync-assets.mjs             # Mirrors src/ui-ux-pro-max/* into cli/assets/*
│   └── bump.mjs                    # Atomic version bump across all manifest files
├── package.json                    # `bun build src/index.ts --outdir dist --target node`
└── tsconfig.json

.claude/skills/ui-ux-pro-max/       # In-repo Claude Code skill (this repo dogfoods itself)
├── SKILL.md                        # Pre-rendered for Claude Code
├── data    -> ../../../src/ui-ux-pro-max/data       (symlink)
└── scripts -> ../../../src/ui-ux-pro-max/scripts    (symlink)

src/deps-ai-os/                     # DÉPS AI Operating System — independent engine
├── data/                           # Référentiel CSV
│   ├── modules.csv                 # 22 modules: objectif, entrées, méthode, sorties,
│   │                               #   amont/aval, portes QA, pièges
│   ├── pipelines.csv               # 8 parcours pré-câblés
│   ├── formules.csv                # 24 formules normalisées (seuils qualifiés INDICATIF)
│   ├── parametres-politique.csv    # 22 paramètres de politique + statut de validation
│   ├── controles-qa.csv            # 28 contrôles qualité, 19 bloquants
│   └── nomenclature.csv            # Conventions de nommage des livrables
├── scripts/
│   ├── deps_core.py                # Chargement CSV, BM25 sans accents, chaînes, doctor()
│   │                               #   (nommé deps_core et non core: les deux moteurs
│   │                               #   coexistent dans une même exécution pytest)
│   └── deps.py                     # CLI (route, module, pipeline, params, formule, qa,
│                                   #   preflight, nomenclature, doctor)
├── references/                     # Doctrine par domaine (6 documents)
└── tests/test_deps_ai_os.py        # 39 tests: intégrité, routage, invariants

.claude/skills/deps-ai-os/          # In-repo skill (dogfooding)
├── SKILL.md
├── data       -> ../../../src/deps-ai-os/data          (symlink)
├── scripts    -> ../../../src/deps-ai-os/scripts       (symlink)
└── references -> ../../../src/deps-ai-os/references    (symlink)

.claude/skills/                     # Sibling design skills bundled with this repo:
                                    #   banner-design, brand, design, design-system,
                                    #   slides, ui-styling
.claude-plugin/                     # Claude marketplace publishing
├── plugin.json                     # Points at ./.claude/skills/ui-ux-pro-max
└── marketplace.json
skill.json                          # Cross-assistant skill manifest
.github/workflows/                  # claude.yml, claude-code-review.yml,
                                    # python-ci.yml (flake8 + pytest + deps doctor),
                                    # cli-sync-check.yml
docs/, preview/, screenshots/       # Marketing/demo assets — not consumed by code
```

The search engine ranks documents with BM25 (`k1=1.5`, `b=0.75`) on a configured subset of CSV columns; output columns are also configured per domain. Stack searches share a common column schema (`Category`, `Guideline`, `Description`, `Do`, `Don't`, `Code Good`, `Code Bad`, `Severity`, `Docs URL`).

## CLI

```bash
# Install for a specific assistant (or auto-detect)
npx uipro-cli init --ai claude
npx uipro-cli init --ai cursor --force
npx uipro-cli init --ai all --global     # install to ~/ instead of cwd

# Other commands
npx uipro-cli versions
npx uipro-cli update --ai claude
npx uipro-cli uninstall --ai claude [--global]
```

Supported `--ai` values (`AI_TYPES` in `cli/src/types/index.ts`): `claude`, `cursor`, `windsurf`, `antigravity`, `copilot`, `roocode`, `kiro`, `codex`, `qoder`, `gemini`, `trae`, `opencode`, `continue`, `codebuddy`, `droid`, `kilocode`, `warp`, `augment`, `all`.

Each platform's target folders are defined in `AI_FOLDERS` (e.g. `claude → .claude`, `droid → .factory`, `copilot → .github`, `antigravity → .agents`). `init` is template-based by default: it loads `templates/platforms/<platform>.json`, renders `templates/base/skill-content.md` (+ `quick-reference.md` if the platform opts in), and copies `data/` + `scripts/` into the rendered skill directory so installs are self-contained.

## Sync Rules

**Source of truth:** `src/ui-ux-pro-max/`. Never edit files inside `cli/assets/` or inside the in-repo `.claude/skills/ui-ux-pro-max/SKILL.md` directly.

1. **Data & scripts** — edit in `src/ui-ux-pro-max/{data,scripts}/`. The in-repo Claude skill picks them up automatically via the `data` and `scripts` symlinks inside `.claude/skills/ui-ux-pro-max/`.

2. **Templates** — edit in `src/ui-ux-pro-max/templates/`:
   - `base/skill-content.md` — shared SKILL.md body. Placeholders: `{{TITLE}}`, `{{DESCRIPTION}}`, `{{SCRIPT_PATH}}`, `{{SKILL_OR_WORKFLOW}}`, `{{QUICK_REFERENCE}}`.
   - `base/quick-reference.md` — appended for platforms with `"sections.quickReference": true` (currently only Claude).
   - `platforms/*.json` — one config per assistant: `folderStructure`, `scriptPath`, `frontmatter`, `title`, `description`, `skillOrWorkflow`.

3. **CLI assets** — `cli/assets/{data,scripts,templates}/` are **generated** from `src/ui-ux-pro-max/` and are gitignored. They are repopulated automatically by:
   - `npm install` in `cli/` (via the `prepare` lifecycle hook)
   - `npm pack` / `npm publish` (via `prepare`)
   - manually: `npm run sync` (alias for `node scripts/sync-assets.mjs`)

   You should never see `cli/assets/data/`, `cli/assets/scripts/`, or `cli/assets/templates/` in `git status`. If you do, you've edited the wrong copy — edit `src/ui-ux-pro-max/` instead and re-run sync.

4. **In-repo `.claude/skills/ui-ux-pro-max/SKILL.md`** — this file is pre-rendered output, used to dogfood the skill in this repo. Never hand-edit it; after changing templates, regenerate it with:

   ```bash
   node cli/scripts/render-skill.mjs claude --write .claude/skills/ui-ux-pro-max/SKILL.md
   ```

   CI (`cli-sync-check.yml`) fails if this file drifts from the templates (`render-skill.mjs claude --check`). The script mirrors the substitution rules of `cli/src/utils/template.ts` — keep the two in sync when changing either.

   **`.claude/skills/deps-ai-os/SKILL.md` is different**: it is hand-written, not template-rendered, because the DÉPS AI OS is not distributed through the npm CLI. Edit it directly. Its `data`, `scripts` and `references` symlinks point at `src/deps-ai-os/`, so the referential and the engine are edited only there. The DÉPS engine is deliberately **not** mirrored into `cli/assets/` and is not touched by `npm run sync`.

5. **Version bumps** — `cli/package.json`, `skill.json`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` all carry the version. Bump them atomically:

   ```bash
   node cli/scripts/bump.mjs 2.5.1     # or: cd cli && npm run release 2.5.1
   git diff                            # review
   git commit -am "chore: release v2.5.1"
   git tag v2.5.1
   ```

## Building the CLI

```bash
cd cli
npm install            # runs `prepare` -> populates cli/assets/ from src/ui-ux-pro-max/
npm run sync           # re-sync assets manually after editing src/
npm run dev -- init    # run from source
npm run build          # bun build src/index.ts --outdir dist --target node
npm run release 2.5.1  # atomic version bump across all manifest files
```

The published package ships `dist/` + `assets/` (see `cli/package.json` `files`). `assets/` is generated, not checked in.

## Prerequisites

- Python 3.x (no external dependencies — only stdlib `csv`, `re`, `math`, `pathlib`, `collections`, `unicodedata`).
- Node.js + Bun (for working on the CLI). End users of `npx uipro-cli` only need Node.
- `pytest` only to run the DÉPS AI OS test suite locally (`pytest src/deps-ai-os/tests -q`); the engines themselves need nothing beyond the stdlib.

## CI

- `.github/workflows/python-ci.yml` — on Python 3.10 and 3.12: `flake8` over the whole repo (syntax errors fail the build; style warnings exit-zero), then `pytest` over `tests/` (engine smoke tests + CSV structural validation — every CSV row must match its header's field count), `.claude/skills/ui-styling/scripts/tests` and `src/deps-ai-os/tests`, and finally `deps.py doctor`, which exits 1 on any DÉPS referential inconsistency.
- `.github/workflows/cli-sync-check.yml` — guards the sync rules: `cli/assets/` subdirs must not be tracked, regenerated assets must mirror `src/ui-ux-pro-max/`, the in-repo SKILL.md must match the templates (`render-skill.mjs claude --check`), and all four manifest versions must be aligned.
- `.github/workflows/claude.yml`, `claude-code-review.yml` — Claude Code GitHub App workflows (need `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` as a repo secret).

## Git Workflow

Never push directly to `main`. Always:

1. Create a branch: `git checkout -b feat/...` or `fix/...` (other common prefixes in history: `chore/`, `add-`, naming is not strictly enforced).
2. Commit with a conventional-style message (`feat(scope): …`, `fix(scope): …`, `chore: …` are used throughout the log).
3. Push: `git push -u origin <branch>`.
4. Open a PR.
