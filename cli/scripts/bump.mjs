#!/usr/bin/env node
// Bump version atomically across all four version-bearing files:
//   cli/package.json
//   skill.json
//   .claude-plugin/plugin.json
//   .claude-plugin/marketplace.json (top-level + plugin entries)
//
// Usage:  node scripts/bump.mjs <new-version>
//         node scripts/bump.mjs 2.5.1

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..', '..');

const newVersion = process.argv[2];
if (!newVersion || !/^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$/.test(newVersion)) {
  console.error('Usage: node scripts/bump.mjs <semver>');
  console.error('Example: node scripts/bump.mjs 2.5.1');
  process.exit(1);
}

function patchJson(relPath, mutate) {
  const abs = join(repoRoot, relPath);
  const raw = readFileSync(abs, 'utf-8');
  const json = JSON.parse(raw);
  const before = JSON.stringify(json);
  mutate(json);
  const after = JSON.stringify(json);
  if (before === after) {
    console.log(`  = ${relPath} (already ${newVersion})`);
    return;
  }
  // Preserve trailing newline if the original had one.
  const trailing = raw.endsWith('\n') ? '\n' : '';
  writeFileSync(abs, JSON.stringify(json, null, 2) + trailing);
  console.log(`  ✓ ${relPath}`);
}

console.log(`Bumping to ${newVersion}:`);

patchJson('cli/package.json', (j) => {
  j.version = newVersion;
});

patchJson('skill.json', (j) => {
  j.version = newVersion;
});

patchJson('.claude-plugin/plugin.json', (j) => {
  j.version = newVersion;
});

patchJson('.claude-plugin/marketplace.json', (j) => {
  if (j.metadata) j.metadata.version = newVersion;
  if (Array.isArray(j.plugins)) {
    for (const p of j.plugins) p.version = newVersion;
  }
});

console.log('\nDone. Review with `git diff`, then commit and tag:');
console.log(`  git commit -am "chore: release v${newVersion}"`);
console.log(`  git tag v${newVersion}`);
