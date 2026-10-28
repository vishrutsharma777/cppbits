// Checks every problem with the same compiler, flags and runtime as the website:
//  * the reference solution compiles without warnings and passes all tests;
//  * the starter code does NOT pass;
//  * for predict-the-output questions, the program prints exactly the expected output.
// usage: node tools/grade.mjs <bundle.js> [--pch] [--only id1,id2]
import { pathToFileURL, fileURLToPath } from 'node:url';
import { readFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { runClang } = await import(pathToFileURL(process.argv[2]).href);
const { makeJob, parseResult, sameOutput } = await import(pathToFileURL(join(root, 'site/cc/jobs.js')).href);
const { runWasi } = await import(pathToFileURL(join(root, 'site/cc/wasi-shim.js')).href);
const usePch = process.argv.includes('--pch');
const oi = process.argv.indexOf('--only');
const only = oi > 0 ? new Set(process.argv[oi + 1].split(',')) : null;

const data = JSON.parse(readFileSync(join(root, 'build/problems.json'), 'utf8'));
const assets = { checkH: data.check_h };
if (usePch) {
  assets.pch = readFileSync(join(root, 'build/pre.hpp.pch'));
  assets.preHpp = readFileSync(join(root, 'site/cc/pre.hpp'), 'utf8');
}

async function compile(job) {
  const { args, files, usedPch } = makeJob(job, assets);
  let log = '';
  const opts = { stderr: b => { if (b) log += new TextDecoder().decode(b); }, stdout: b => { if (b) log += new TextDecoder().decode(b); }, fetchProgress: () => {} };
  const t = Date.now();
  try {
    const out = await runClang(args, files, opts);
    return { ok: true, wasm: out['a.wasm'], log, ms: Date.now() - t, usedPch };
  } catch (e) {
    return { ok: false, log: log || String(e), ms: Date.now() - t, usedPch };
  }
}

async function judge(p, code) {
  if (p.kind === 'predict') {
    // the "solution" is the program shown on the page; the "starter" is the empty answer
    if (code === p.starter) return { verdict: sameOutput(p.starter, p.expected) ? 'pass' : 'wrong answer', log: '', ms: 0 };
    const c = await compile({ lang: p.lang, kind: 'stdout', code });
    if (!c.ok) return { verdict: 'compile error', log: c.log, ms: c.ms };
    const r = runWasi(await WebAssembly.compile(c.wasm), {});
    if (r.trap) return { verdict: 'trap: ' + r.trap, log: c.log, ms: c.ms, run: r };
    const good = sameOutput(r.stdout, p.expected);   // the page ignores trailing spaces the same way
    return { verdict: good ? 'pass' : 'wrong output', log: c.log, ms: c.ms, run: { stdout: `\n   expected: ${JSON.stringify(p.expected)}\n   got:      ${JSON.stringify(r.stdout)}` } };
  }
  const c = await compile({ lang: p.lang, kind: p.kind, code, test: p.test });
  if (!c.ok) return { verdict: 'compile error', log: c.log, ms: c.ms };
  const mod = await WebAssembly.compile(c.wasm);
  const r = runWasi(mod, {});
  if (p.kind === 'stdout') {
    const good = r.trap == null && sameOutput(r.stdout, p.expected);
    return { verdict: good ? 'pass' : 'wrong output', log: c.log, ms: c.ms, run: r };
  }
  const res = parseResult(r.stdout);
  if (r.trap) return { verdict: 'trap: ' + r.trap, log: c.log, ms: c.ms, run: r, res };
  if (!res.done) return { verdict: 'no result line', log: c.log, ms: c.ms, run: r, res };
  return { verdict: res.pass === res.total && res.total > 0 ? 'pass' : `fail ${res.pass}/${res.total}`, log: c.log, ms: c.ms, run: r, res };
}

await runClang(['clang', 'x.c', '-c', '-o', 'x.o'], { 'x.c': 'int x;' }, { stderr: () => {}, stdout: () => {}, fetchProgress: () => {} });
let problems = 0, bad = 0;
const times = [];
for (const p of data.problems) {
  if (only && !only.has(p.id)) continue;
  problems++;
  const s = await judge(p, p.solution);
  const st = await judge(p, p.starter);
  times.push([p.id, s.ms]);
  // predict questions may warn on purpose (the warning is part of the lesson); print it instead
  const okSol = s.verdict === 'pass' && (p.kind === 'predict' || !/warning|error/.test(s.log));
  const okStart = st.verdict !== 'pass';
  const line = `${okSol && okStart ? 'ok  ' : 'BAD '} ${p.id.padEnd(16)} solution: ${s.verdict} (${s.ms} ms${s.res ? ', ' + s.res.total + ' checks' : ''})  starter: ${st.verdict}`;
  console.log(line);
  if (p.kind === 'predict' && s.log) console.log('   (warning shown to the reader) ' + s.log.split('\n')[0].slice(0, 160));
  if (!okSol || !okStart) {
    bad++;
    if (s.log) console.log('   solution log:', s.log.slice(0, 1500));
    if (s.res && s.res.mismatches.length) console.log('   mismatches:', s.res.mismatches.slice(0, 3).join('\n                '));
    if (s.run && s.run.stdout && s.verdict !== 'pass') console.log('   stdout:', s.run.stdout.slice(0, 500));
  }
}
times.sort((a, b) => b[1] - a[1]);
console.log(`\n${problems} problems, ${bad} bad. pch=${usePch}. slowest compiles:`, times.slice(0, 5).map(t => t.join(' ')).join(', '));
