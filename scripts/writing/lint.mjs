#!/usr/bin/env node
// Cross-platform wrapper; dependencies are installed explicitly, never by this script.
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = dirname(fileURLToPath(import.meta.url));
const files = process.argv.slice(2);
if (!files.length || files.some(file => file.startsWith('-'))) {
  console.error('Usage: node scripts/writing/lint.mjs draft.md [another.md ...]');
  process.exit(2);
}
for (const file of files) {
  if (!existsSync(file)) { console.error(`Cannot read ${file}`); process.exit(2); }
}
const manifest = resolve(root, 'node_modules/slopless/package.json');
let ast;
if (existsSync(manifest)) {
  const { readFileSync } = await import('node:fs');
  const pkg = JSON.parse(readFileSync(manifest, 'utf8'));
  ast = resolve(dirname(manifest), typeof pkg.bin === 'string' ? pkg.bin : pkg.bin.slopless);
}
let status = 0;
for (const [name, script] of [['Slopless AST', ast], ['OMP cliche patterns', resolve(root, 'cliche-lint.mjs')]]) {
  if (!script || !existsSync(script)) {
    console.error(`${name} unavailable. Run npm install --prefix scripts/writing --ignore-scripts first.`);
    status = 2;
    continue;
  }
  console.log(`Checking ${name}`);
  const result = spawnSync(process.execPath, [script, ...files], { stdio: 'inherit' });
  status = Math.max(status, result.error || result.status === null ? 2 : Math.min(result.status, 2));
}
process.exit(status);
