// Runs one compiled program. The page terminates this worker if it takes too long.
import { runWasi } from './wasi-shim.js';

self.onmessage = async (ev) => {
  const { wasm, stdin } = ev.data;
  try {
    const module = await WebAssembly.compile(wasm);
    self.postMessage({ type: 'result', ...runWasi(module, { stdin: stdin || '' }) });
  } catch (e) {
    self.postMessage({ type: 'result', stdout: '', stderr: '', exitCode: -1, trap: 'Could not start the program: ' + (e && e.message || e), ms: 0 });
  }
};
