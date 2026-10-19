# Third-party software

| Component | Where | Licence |
|---|---|---|
| LLVM / Clang / LLD 22 (compiled to WebAssembly) | `site/cc/llvm.core*.wasm*`, `site/cc/bundle.js` | Apache License 2.0 with LLVM Exceptions, <https://llvm.org/LICENSE.txt> |
| libc++, libc++abi, compiler-rt (in the sysroot) | `site/cc/llvm-resources.tar.gz0.wasm` | Apache License 2.0 with LLVM Exceptions |
| wasi-libc (in the sysroot) | `site/cc/llvm-resources.tar.gz0.wasm` | Apache 2.0 with LLVM Exception / MIT / CC0 (see <https://github.com/WebAssembly/wasi-libc/blob/main/LICENSE>) |
| YoWASP Clang packaging and JavaScript runtime | `site/cc/bundle.js` | ISC, <https://github.com/YoWASP/clang>, <https://github.com/YoWASP/runtime-js> |
| CodeMirror 5.65.16 | stylesheet in `vendor/` and inlined in `site/index.html`; scripts loaded from cdnjs | MIT, <https://github.com/codemirror/codemirror5/blob/master/LICENSE> |
| IBM Plex fonts | loaded from Google Fonts | SIL Open Font License 1.1 |

The compiler files come unmodified from the npm package `@yowasp/clang@22.0.0-git20542-10`;
the large ones are gzip-compressed and split into chunks.
