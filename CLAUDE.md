# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI/UX Pro Max is an AI design-intelligence toolkit distributed as a skill / workflow for AI coding assistants (Claude Code, Cursor, Windsurf, Copilot, Droid/Factory, Codex, Gemini, Kiro, Roo Code, Qoder, Trae, OpenCode, Continue, CodeBuddy, KiloCode, Warp, Augment, Antigravity).

It ships:

- A **Python search engine** (`src/ui-ux-pro-max/scripts/`) that runs offline with no external dependencies — BM25 + regex over CSV knowledge bases for styles, color palettes, typography, charts, UX guidelines, icons, and per-stack best practices.
- A **design-system generator** that aggregates multiple searches and applies reasoning rules from `ui-reasoning.csv` to recommend a complete design system (pattern + style + colors + typography + effects + anti-patterns).
- An **npm CLI (`uipro-cli`)** in `cli/` that installs the skill into any of ~18 supported AI assistants by rendering platform-specific templates and copying the data + scripts into the right folder (`.claude/`, `.cursor/`, `.windsurf/`, `.factory/`, `.codex/`, …).
- A **Claude marketplace plugin** packaged via `.claude-plugin/`.

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

## Architecture

```
src/ui-ux-pro-max/                  # Source of truth
├── data/                           # Canonical CSV knowledge bases
│   ├── products.csv, styles.csv, colors.csv, typography.csv,
│   ├── charts.csv, landing.csv, ux-guidelines.csv, icons.csv,
│   ├── google-fonts.csv, ui-reasoning.csv, react-performance.csv,
│   ├── app-interface.csv, design.csv, draft.csv
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
├── assets/                         # Bundled copy of src/ui-ux-pro-max/{data,scripts,templates}
├── package.json                    # `bun build src/index.ts --outdir dist --target node`
└── tsconfig.json

.claude/skills/ui-ux-pro-max/       # In-repo Claude Code skill (this repo dogfoods itself)
├── SKILL.md                        # Pre-rendered for Claude Code
├── data    -> ../../../src/ui-ux-pro-max/data       (symlink)
└── scripts -> ../../../src/ui-ux-pro-max/scripts    (symlink)

.claude/skills/                     # Sibling design skills bundled with this repo:
                                    #   banner-design, brand, design, design-system,
                                    #   slides, ui-styling
.claude-plugin/                     # Claude marketplace publishing
├── plugin.json                     # Points at ./.claude/skills/ui-ux-pro-max
└── marketplace.json
skill.json                          # Cross-assistant skill manifest
.github/workflows/                  # claude.yml, claude-code-review.yml,
                                    # python-package-conda.yml (flake8 + pytest)
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

3. **CLI assets** — `cli/assets/` is a copy of `src/ui-ux-pro-max/{data,scripts,templates}/` and must be re-synced before publishing the npm package:

   ```bash
   cp -r src/ui-ux-pro-max/data/*      cli/assets/data/
   cp -r src/ui-ux-pro-max/scripts/*   cli/assets/scripts/
   cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/
   ```

4. **In-repo `.claude/skills/ui-ux-pro-max/SKILL.md`** — this file is pre-rendered output, used to dogfood the skill in this repo. Regenerate it from the templates (e.g. by running `uipro init --ai claude --force` in a scratch dir and copying the result back) rather than hand-editing.

5. **Version bumps** — when releasing, keep `cli/package.json`, `skill.json`, and `.claude-plugin/plugin.json` aligned. (`.claude-plugin/marketplace.json` is currently pinned to an older `2.2.1` — leave it unless explicitly updating the marketplace listing.)

## Building the CLI

```bash
cd cli
bun install            # or: npm install
bun run dev -- init    # run from source
bun run build          # bun build src/index.ts --outdir dist --target node
```

The published package ships `dist/` + `assets/` (see `cli/package.json` `files`).

## Prerequisites

- Python 3.x (no external dependencies — only stdlib `csv`, `re`, `math`, `pathlib`, `collections`).
- Node.js + Bun (for working on the CLI). End users of `npx uipro-cli` only need Node.

## CI

- `.github/workflows/python-package-conda.yml` — runs `flake8` (syntax errors fail the build; style warnings exit-zero) and `pytest` against the Python code.
- `.github/workflows/claude.yml`, `claude-code-review.yml` — Claude Code GitHub App workflows.

## Git Workflow

Never push directly to `main`. Always:

1. Create a branch: `git checkout -b feat/...` or `fix/...` (other common prefixes in history: `chore/`, `add-`, naming is not strictly enforced).
2. Commit with a conventional-style message (`feat(scope): …`, `fix(scope): …`, `chore: …` are used throughout the log).
3. Push: `git push -u origin <branch>`.
4. Open a PR.
