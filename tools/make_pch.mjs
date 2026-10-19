// Builds site/cc/pre.hpp.pch with the same clang (YoWASP) and flags the site uses.
// usage: node tools/make_pch.mjs <path to @yowasp/clang gen/bundle.js>
import { pathToFileURL, fileURLToPath } from 'node:url';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { runClang } = await import(pathToFileURL(process.argv[2]).href);
const { CXX_FLAGS, UB_FLAGS } = await import(pathToFileURL(join(root, 'site/cc/jobs.js')).href);
const hdr = readFileSync(join(root, 'site/cc/pre.hpp'), 'utf8');
let log = '';
const t = Date.now();
const r = await runClang(['clang++', ...CXX_FLAGS, ...UB_FLAGS, '-x', 'c++-header', 'pre.hpp', '-o', 'pre.hpp.pch'],
  { 'pre.hpp': hdr }, { stderr: b => { if (b) log += new TextDecoder().decode(b); }, stdout: () => {}, fetchProgress: () => {} });
writeFileSync(join(root, 'build/pre.hpp.pch'), r['pre.hpp.pch']);
console.log('pch', r['pre.hpp.pch'].length, 'bytes in', Date.now() - t, 'ms', log);
