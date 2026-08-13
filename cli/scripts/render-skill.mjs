#!/usr/bin/env node
// Renders a platform SKILL file from src/ui-ux-pro-max/templates/, mirroring
// the substitution rules of cli/src/utils/template.ts (renderFrontmatter +
// renderSkillFile). Keep the two in sync when changing either.
//
// Usage:
//   node cli/scripts/render-skill.mjs <platform> --write <path>   # render and write
//   node cli/scripts/render-skill.mjs <platform> --check <path>   # diff against file, exit 1 on drift
//
// The in-repo dogfood copy is regenerated with:
//   node cli/scripts/render-skill.mjs claude --write .claude/skills/ui-ux-pro-max/SKILL.md

import { readFile, writeFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const TEMPLATES = join(ROOT, 'src', 'ui-ux-pro-max', 'templates');

function renderFrontmatter(frontmatter) {
  if (!frontmatter) return '';
  const lines = ['---'];
  for (const [key, value] of Object.entries(frontmatter)) {
    if (value.includes(':') || value.includes('"') || value.includes('\n')) {
      lines.push(`${key}: "${value.replace(/"/g, '\\"')}"`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  lines.push('---', '');
  return lines.join('\n');
}

async function render(platform) {
  const config = JSON.parse(
    await readFile(join(TEMPLATES, 'platforms', `${platform}.json`), 'utf-8')
  );
  let content = await readFile(join(TEMPLATES, 'base', 'skill-content.md'), 'utf-8');

  let quickReferenceContent = '';
  if (config.sections.quickReference) {
    quickReferenceContent = await readFile(join(TEMPLATES, 'base', 'quick-reference.md'), 'utf-8');
  }
  const quickRefWithNewline = quickReferenceContent ? '\n' + quickReferenceContent : '';

  content = content
    .replace(/\{\{TITLE\}\}/g, config.title)
    .replace(/\{\{DESCRIPTION\}\}/g, config.description)
    .replace(/\{\{SCRIPT_PATH\}\}/g, config.scriptPath)
    .replace(/\{\{SKILL_OR_WORKFLOW\}\}/g, config.skillOrWorkflow)
    .replace(/\{\{QUICK_REFERENCE\}\}/g, quickRefWithNewline);

  return renderFrontmatter(config.frontmatter) + content;
}

const [platform, mode, target] = process.argv.slice(2);
if (!platform || !['--write', '--check'].includes(mode) || !target) {
  console.error('Usage: render-skill.mjs <platform> --write|--check <path>');
  process.exit(2);
}

const rendered = await render(platform);
const targetPath = join(ROOT, target);

if (mode === '--write') {
  await writeFile(targetPath, rendered, 'utf-8');
  console.log(`Rendered ${platform} -> ${target}`);
} else {
  const existing = await readFile(targetPath, 'utf-8');
  if (existing !== rendered) {
    const a = rendered.split('\n');
    const b = existing.split('\n');
    for (let i = 0; i < Math.max(a.length, b.length); i++) {
      if (a[i] !== b[i]) {
        console.error(`First divergence at line ${i + 1}:`);
        console.error(`  rendered: ${a[i] ?? '<EOF>'}`);
        console.error(`  on disk:  ${b[i] ?? '<EOF>'}`);
        break;
      }
    }
    console.error(
      `DRIFT: ${target} does not match the templates. ` +
      `Regenerate it with: node cli/scripts/render-skill.mjs ${platform} --write ${target}`
    );
    process.exit(1);
  }
  console.log(`OK: ${target} matches the templates.`);
}
