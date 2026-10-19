// Compiler worker: loads clang/LLD (YoWASP, compiled to WebAssembly) and compiles C/C++ to WASI programs.
// The big files are stored as gzip chunks next to this file; fetch() is patched so the bundle
// receives the original files. Downloads are cached in IndexedDB, so later visits start fast.
import { makeJob } from './jobs.js';

const VERSION = 'clang-22.0.0-git20542-10-r1';
// Filled from manifest.json (written by tools/package.py):
// files: original name -> { parts: [gzip chunk names], type }, sizes: chunk name -> bytes
const MANIFEST = {};
const SIZES = {};
const base = new URL('./', self.location.href);
// the bundle logs download progress to the console; the page shows its own progress instead
const consoleLog = console.log.bind(console);
console.log = (...a) => { if (!(typeof a[0] === 'string' && a[0].startsWith('yowasp-'))) consoleLog(...a); };
const realFetch = self.fetch.bind(self);

// ---------- IndexedDB cache (optional: every call is allowed to fail) ----------
let dbp = null;
function db() {
  if (!dbp) dbp = new Promise((res) => {
    try {
      const r = indexedDB.open('cppbits-cache', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('files');
      r.onsuccess = () => res(r.result);
      r.onerror = () => res(null);
    } catch (e) { res(null); }
  });
  return dbp;
}
async function cacheGet(key) {
  const d = await db(); if (!d) return null;
  return new Promise((res) => {
    try { const q = d.transaction('files').objectStore('files').get(VERSION + '/' + key); q.onsuccess = () => res(q.result || null); q.onerror = () => res(null); }
    catch (e) { res(null); }
  });
}
async function cachePut(key, buf) {
  const d = await db(); if (!d) return;
  try { d.transaction('files', 'readwrite').objectStore('files').put(buf, VERSION + '/' + key); } catch (e) { /* quota or private mode */ }
}

// ---------- downloads with progress ----------
let loaded = 0, total = 0;
function progress(stage) { self.postMessage({ type: 'progress', stage, loaded, total }); }

async function fetchPart(name) {
  const cached = await cacheGet(name);
  if (cached) { loaded += cached.byteLength; progress('cache'); return new Uint8Array(cached); }
  const resp = await realFetch(new URL(name, base));
  if (!resp.ok) throw new Error(`Could not download ${name} (HTTP ${resp.status})`);
  const reader = resp.body.getReader();
  const chunks = []; let n = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value); n += value.length; loaded += value.length; progress('download');
  }
  const out = new Uint8Array(n); let o = 0;
  for (const c of chunks) { out.set(c, o); o += c.length; }
  cachePut(name, out.buffer);
  return out;
}

async function gunzip(bytes) {
  if (bytes[0] !== 0x1f || bytes[1] !== 0x8b) return bytes;   // already decoded by the server
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

async function loadFile(name) {
  const parts = [];
  for (const p of MANIFEST[name].parts) parts.push(await fetchPart(p));
  let n = 0; for (const p of parts) n += p.length;
  const all = new Uint8Array(n); let o = 0;
  for (const p of parts) { all.set(p, o); o += p.length; }
  return gunzip(all);
}

self.fetch = async (input, init) => {
  const url = input instanceof URL ? input : new URL(typeof input === 'string' ? input : input.url, base);
  const name = url.pathname.split('/').pop();
  if (MANIFEST[name]) {
    const data = await loadFile(name);
    return new Response(data, { headers: { 'content-type': MANIFEST[name].type, 'content-length': String(data.length) } });
  }
  return realFetch(input, init);
};

// ---------- start-up ----------
let runClang = null;
let pch = null, preHpp = null;
const quiet = { stdout: () => {}, stderr: () => {}, fetchProgress: () => {} };

async function start() {
  try {
    const man = await (await realFetch(new URL('manifest.json', base))).json();
    Object.assign(MANIFEST, man.files);
    Object.assign(SIZES, man.sizes);
    for (const f of ['llvm.core.wasm', 'llvm-resources.tar']) for (const p of MANIFEST[f].parts) total += SIZES[p] || 0;
    progress('download');
    ({ runClang } = await import('./bundle.js'));
    await runClang(['clang', '-c', 'warm.c', '-o', 'warm.o'], { 'warm.c': 'int warm;' }, quiet);
    self.postMessage({ type: 'ready' });
  } catch (e) {
    self.postMessage({ type: 'fatal', message: String(e && e.message || e) });
    return;
  }
  try {   // the precompiled header only speeds up C++; failure is not fatal
    loaded = 0; total = 0;
    for (const p of MANIFEST['pre.hpp.pch'].parts) total += SIZES[p] || 0;
    preHpp = await (await realFetch(new URL('pre.hpp', base))).text();
    pch = await loadFile('pre.hpp.pch');
    self.postMessage({ type: 'pch-ready' });
  } catch (e) {
    self.postMessage({ type: 'pch-failed', message: String(e && e.message || e) });
  }
}

// ---------- compile requests (one at a time) ----------
let queue = Promise.resolve();
self.onmessage = (ev) => {
  const msg = ev.data;
  if (msg.type !== 'compile') return;
  queue = queue.then(async () => {
    let log = '';
    const dec = new TextDecoder();
    const t0 = performance.now();
    const { args, files, usedPch } = makeJob(msg.job, { checkH: msg.checkH, pch, preHpp });
    try {
      const out = await runClang(args, files, {
        stdout: (b) => { if (b) log += dec.decode(b); },
        stderr: (b) => { if (b) log += dec.decode(b); },
        fetchProgress: () => {},
      });
      const wasm = out['a.wasm'];
      self.postMessage({ type: 'compiled', id: msg.id, ok: true, wasm, log, ms: performance.now() - t0, usedPch, args }, [wasm.buffer]);
    } catch (e) {
      if (!log) log = String(e && e.message || e);
      self.postMessage({ type: 'compiled', id: msg.id, ok: false, log, ms: performance.now() - t0, usedPch, args });
    }
  });
};

start();
