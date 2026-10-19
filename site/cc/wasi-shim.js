// Minimal WASI preview1 runtime for programs compiled by clang (wasm32-wasip1).
// Supports stdin/stdout/stderr, clocks, random and exit; everything else returns ENOSYS.
// Used by runner-worker.js in the browser and by the Node grader.

const ESUCCESS = 0, EBADF = 8, EINVAL = 28, ENOSYS = 52, ESPIPE = 70;

export class ProcExit extends Error {
  constructor(code) { super('exit ' + code); this.code = code; }
}

export function runWasi(module, { stdin = '', maxOutput = 200000, onOutput = null } = {}) {
  const enc = new TextEncoder();
  const stdinBytes = enc.encode(stdin);
  let stdinPos = 0;
  const out = [], err = [];
  let outLen = 0, truncated = false;
  let memory = null;
  const view = () => new DataView(memory.buffer);
  const bytes = () => new Uint8Array(memory.buffer);

  function writeFd(fd, chunk) {
    if (outLen + chunk.length > maxOutput) {
      chunk = chunk.slice(0, Math.max(0, maxOutput - outLen));
      truncated = true;
    }
    outLen += chunk.length;
    (fd === 1 ? out : err).push(chunk);
    if (onOutput) onOutput(fd, chunk);
  }

  const imp = {
    args_sizes_get(argcPtr, bufSizePtr) { const v = view(); v.setUint32(argcPtr, 1, true); v.setUint32(bufSizePtr, 5, true); return ESUCCESS; },
    args_get(argvPtr, bufPtr) { const v = view(); v.setUint32(argvPtr, bufPtr, true); bytes().set(enc.encode('prog\0'), bufPtr); return ESUCCESS; },
    environ_sizes_get(cPtr, sPtr) { const v = view(); v.setUint32(cPtr, 0, true); v.setUint32(sPtr, 0, true); return ESUCCESS; },
    environ_get() { return ESUCCESS; },
    clock_res_get(id, resPtr) { view().setBigUint64(resPtr, 1000n, true); return ESUCCESS; },
    clock_time_get(id, precision, timePtr) {
      const ns = id === 0 ? BigInt(Date.now()) * 1000000n : BigInt(Math.round(performance.now() * 1e6));
      view().setBigUint64(timePtr, ns, true);
      return ESUCCESS;
    },
    fd_write(fd, iovs, iovsLen, nwrittenPtr) {
      if (fd !== 1 && fd !== 2) return EBADF;
      const v = view(); let n = 0;
      for (let i = 0; i < iovsLen; i++) {
        const p = v.getUint32(iovs + 8 * i, true), len = v.getUint32(iovs + 8 * i + 4, true);
        writeFd(fd, bytes().slice(p, p + len));
        n += len;
      }
      v.setUint32(nwrittenPtr, n, true);
      return ESUCCESS;
    },
    fd_read(fd, iovs, iovsLen, nreadPtr) {
      if (fd !== 0) return EBADF;
      const v = view(); let n = 0;
      for (let i = 0; i < iovsLen; i++) {
        const p = v.getUint32(iovs + 8 * i, true), len = v.getUint32(iovs + 8 * i + 4, true);
        const take = Math.min(len, stdinBytes.length - stdinPos);
        bytes().set(stdinBytes.subarray(stdinPos, stdinPos + take), p);
        stdinPos += take; n += take;
        if (take < len) break;
      }
      v.setUint32(nreadPtr, n, true);
      return ESUCCESS;
    },
    fd_fdstat_get(fd, bufPtr) {
      if (fd > 2) return EBADF;
      const v = view();
      v.setUint8(bufPtr, 2);            // character device
      v.setUint16(bufPtr + 2, 0, true); // flags
      v.setBigUint64(bufPtr + 8, 0xFFFFFFFFn, true);
      v.setBigUint64(bufPtr + 16, 0n, true);
      return ESUCCESS;
    },
    fd_fdstat_set_flags() { return ESUCCESS; },
    fd_filestat_get(fd, bufPtr) {
      if (fd > 2) return EBADF;
      const b = bytes(); b.fill(0, bufPtr, bufPtr + 64); view().setUint8(bufPtr + 16, 2);
      return ESUCCESS;
    },
    fd_prestat_get() { return EBADF; },
    fd_prestat_dir_name() { return EBADF; },
    fd_seek(fd) { return fd <= 2 ? ESPIPE : EBADF; },
    fd_tell(fd) { return fd <= 2 ? ESPIPE : EBADF; },
    fd_close(fd) { return fd <= 2 ? ESUCCESS : EBADF; },
    fd_sync() { return ESUCCESS; },
    random_get(bufPtr, len) {
      const b = bytes();
      for (let off = 0; off < len; off += 65536) {
        const n = Math.min(65536, len - off);
        crypto.getRandomValues(b.subarray(bufPtr + off, bufPtr + off + n));
      }
      return ESUCCESS;
    },
    sched_yield() { return ESUCCESS; },
    poll_oneoff() { return ENOSYS; },
    proc_exit(code) { throw new ProcExit(code); },
    proc_raise() { return ENOSYS; },
  };
  const wasiImport = new Proxy(imp, { get: (t, k) => (k in t ? t[k] : () => ENOSYS) });

  const t0 = performance.now();
  let exitCode = 0, trap = null;
  try {
    const instance = new WebAssembly.Instance(module, { wasi_snapshot_preview1: wasiImport });
    memory = instance.exports.memory;
    instance.exports._start();
  } catch (e) {
    if (e instanceof ProcExit) exitCode = e.code;
    else { trap = String(e && e.message || e); exitCode = -1; }
  }
  const dec = new TextDecoder();
  const join = parts => { let n = 0; for (const p of parts) n += p.length; const r = new Uint8Array(n); let o = 0; for (const p of parts) { r.set(p, o); o += p.length; } return dec.decode(r); };
  return { stdout: join(out), stderr: join(err), exitCode, trap, truncated, ms: performance.now() - t0 };
}
