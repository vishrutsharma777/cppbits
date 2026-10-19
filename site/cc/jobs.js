// Builds the clang command line and virtual files for one compile, and reads test results.
// Shared by compiler-worker.js (browser) and the Node grader, so both compile identically.

export const C_FLAGS = ['-std=c11', '-O1', '-Wall', '-fno-color-diagnostics'];
export const CXX_FLAGS = ['-std=c++20', '-fno-exceptions', '-O1', '-Wall', '-fno-color-diagnostics'];
export const UB_FLAGS = ['-fsanitize=undefined', '-fsanitize-trap=undefined'];

// The precompiled header is built with exactly CXX_FLAGS + UB_FLAGS (see tools/make_pch.mjs).
export function pchUsable(job) {
  return job.lang === 'cpp' && job.ub !== false && !job.std && !job.opt;
}

// job: { lang: 'c'|'cpp', kind: 'func'|'stdout'|'play', code, test?, ub?, std?, opt? }
// assets: { checkH, pch?, preHpp? }
export function makeJob(job, assets) {
  const ext = job.lang === 'c' ? 'c' : 'cpp';
  const files = {};
  files['solution.' + ext] = job.code;
  let main = 'solution.' + ext;
  if (job.kind === 'func') {
    files['test.' + ext] = job.test;
    files['check.h'] = assets.checkH;
    main = 'test.' + ext;
  }
  let flags = (job.lang === 'c' ? C_FLAGS : CXX_FLAGS).slice();
  if (job.std) flags = flags.map(f => (f.startsWith('-std=') ? '-std=' + job.std : f));
  if (job.opt) flags = flags.map(f => (/^-O/.test(f) ? job.opt : f));
  const args = [job.lang === 'c' ? 'clang' : 'clang++', ...flags];
  if (job.ub !== false) args.push(...UB_FLAGS);
  let usedPch = false;
  if (assets.pch && assets.preHpp && pchUsable(job)) {
    files['pre.hpp'] = assets.preHpp;
    files['pre.hpp.pch'] = assets.pch;
    args.push('-include-pch', 'pre.hpp.pch');
    usedPch = true;
  }
  args.push(main, '-o', 'a.wasm');
  return { args, files, usedPch };
}

// Reads the "@@RESULT pass total" and "MISMATCH ..." lines printed by check.h.
export function parseResult(stdout) {
  const m = /@@RESULT (\d+) (\d+)/.exec(stdout);
  const mismatches = stdout.split('\n').filter(l => l.startsWith('MISMATCH ')).map(l => l.slice(9));
  const other = stdout.split('\n').filter(l => !l.startsWith('MISMATCH ') && !l.startsWith('@@RESULT ')).join('\n').replace(/\n+$/, '');
  if (!m) return { done: false, pass: 0, total: 0, mismatches, other };
  return { done: true, pass: +m[1], total: +m[2], mismatches, other };
}

// Output comparison for problems that check what main() prints.
export function sameOutput(got, want) {
  const norm = s => s.replace(/\r\n/g, '\n').split('\n').map(l => l.replace(/\s+$/, '')).join('\n').replace(/\n+$/, '');
  return norm(got) === norm(want);
}
