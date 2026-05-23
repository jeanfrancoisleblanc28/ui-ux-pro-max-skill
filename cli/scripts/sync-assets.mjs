#!/usr/bin/env node
// Mirror src/ui-ux-pro-max/{data,scripts,templates} into cli/assets/.
// Runs automatically via the `prepare` lifecycle (npm install + npm pack/publish).
// Safe to re-run; idempotent.

import { existsSync, rmSync, cpSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const cliDir = resolve(__dirname, '..');
const repoRoot = resolve(cliDir, '..');
const srcRoot = join(repoRoot, 'src', 'ui-ux-pro-max');
const dstRoot = join(cliDir, 'assets');

const dirs = ['data', 'scripts', 'templates'];

// When the package is installed as a dependency, `src/ui-ux-pro-max/` is not
// present and prepare is a no-op (npm doesn't run prepare on consumer installs,
// but be defensive in case a tool does).
if (!existsSync(srcRoot)) {
  console.log(`[sync-assets] ${srcRoot} not found, skipping (consumer install).`);
  process.exit(0);
}

mkdirSync(dstRoot, { recursive: true });

for (const dir of dirs) {
  const from = join(srcRoot, dir);
  const to = join(dstRoot, dir);
  if (!existsSync(from)) {
    console.warn(`[sync-assets] source missing: ${from}`);
    continue;
  }
  rmSync(to, { recursive: true, force: true });
  cpSync(from, to, { recursive: true });
  console.log(`[sync-assets] ${dir}/ -> assets/${dir}/`);
}
