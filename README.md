# CppBits

An [HDLBits](https://hdlbits.01xz.net/)-style practice site for C and C++, aimed at audio and
embedded work. Every problem gives you a function to write; a hidden test program compiles it,
compares it with a reference solution, and lists every mismatch. The compiler is a real
**Clang 22 / LLD**, compiled to WebAssembly, running in your browser, so no server is needed.

160 problems in 15 sections:

| Section | Problems | Examples |
|---|---|---|
| Getting started | 3 | return 1, Hello world, a first loop |
| C basics | 13 | pointers, strings, structs, rounded division, overflow |
| Bits and bytes | 10 | register fields, byte swap, rotate, sign extension, next power of two |
| Pointers and memory | 6 | memcpy, memmove, linked list, malloc |
| Fixed point (Q15 / Q31) | 6 | saturating add, rounded multiply, dot product, gain |
| DSP in C | 15 | dB, RMS, FIR with a circular buffer, biquads (DF1, TDF-II), DC blocker, Goertzel, NLMS |
| Real-time and buffers | 7 | interleave, int16/float, 24-bit unpack, lock-free ring buffer, gain ramps, resampling ratio |
| C++ language | 19 | templates, RAII, move semantics, constexpr, virtual functions, span/optional/function, RBJ biquad class |
| Algorithms | 10 | binary search, two-sum, Kadane, sieve, palindrome, matrix multiply |
| OA: predict the output (C) | 29 | increments, signed/unsigned, `*p++`, `sizeof`, `static`, `const`, padding, macros, recursion in `main` |
| OA: predict the output (C++) | 7 | constructor order, virtual calls, slicing, static members, overloads |
| Embedded C | 10 | UART frames, I2C decoder, CRC-16, Hamming ECC, debounce, watchdog, ISR vector table, memory pool, Gray code |
| OS and architecture in C | 9 | cache split and LRU cache simulator, page tables, FIFO/LRU/optimal paging, FCFS/SJF/RR, Banker's, first/best/worst fit |
| Sorting | 6 | bubble, selection, insertion (with counts), stable merge sort, quicksort on sorted input, `qsort` comparator |
| Interview classics | 10 | 1..n without loops, bits to flip, Floyd cycle, k-th from end, postfix, `strstr`, rotate, `INT_MIN` to string |

The last six sections are placement-OA practice (built for the Qualcomm hardware-engineer OA: C output,
OS, OOP, sorting, embedded). **Predict the output** questions show a program; you type what it prints and
get an explanation. Checking needs no compiler, and **Run it** compiles the program to show the real output.

There is also a **Playground** for running any C or C++ program, with stdin input and a choice
of standard and optimisation level.

## Run it

```
python serve.py
```

Then open <http://localhost:8000>. Any static web server works if it serves `.js` as
`text/javascript` and `.wasm` as `application/wasm`; `serve.py` makes sure of that on Windows.
Opening `site/index.html` directly as a file does **not** work, because browsers start module
workers only from `http(s)://` pages.

The first visit downloads about 27 MB (the compiler), plus 14 MB in the background that makes
C++ compiles faster (about 1 s instead of 6 s). Both are cached in the browser (IndexedDB).
Your solved problems and code are kept in that browser's `localStorage`.

**Online:** <https://vishrutsharma777.github.io/cppbits/>. The workflow in
`.github/workflows/pages.yml` publishes `site/` to GitHub Pages on every push to `main`
(repository Settings → Pages → Source: GitHub Actions).

## How it works

* `site/cc/compiler-worker.js` loads [YoWASP Clang](https://github.com/YoWASP/clang)
  (`@yowasp/clang` 22.0.0-git20542-10) in a Web Worker. The 75 MB `llvm.core.wasm` and the
  sysroot tar are stored gzip-compressed and split into chunks under 15 MB
  (`*.gzN.wasm`; the bytes are gzip, the `.wasm` name is only for hosting).
  `fetch()` is patched so the bundle receives the original files.
* C is compiled with `-std=c11 -O1 -Wall`, C++ with `-std=c++20 -fno-exceptions -O1 -Wall`
  (the bundled libc++ is built without exceptions). Both use
  `-fsanitize=undefined -fsanitize-trap=undefined`, so signed overflow, too-large shifts and
  out-of-range float-to-int conversions stop the program with a runtime error.
* C++ uses a precompiled header (`site/cc/pre.hpp`), built with the same compiler and flags.
* The compiled program runs in `site/cc/runner-worker.js` on a small WASI runtime
  (`site/cc/wasi-shim.js`), with a 5 s time limit.
* Each test program `#include`s the solution and the helpers in `src/check.h`, and prints
  `MISMATCH ...` lines and a final `@@RESULT pass total` line, which the page reads.

## Add or change problems

Problems live in `src/problems_a.py` … `problems_e.py` (statement, starter code, reference solution,
hidden test, hint). Predict-the-output questions use `Q(...)` in `src/common.py`: the program, its
expected output and an HTML explanation; the grader compiles and runs each program and checks the stored
output. Then:

```
python src/build_problems.py                                     # -> build/problems.json
node tools/grade.mjs <path>/gen/bundle.js                         # every solution passes, every starter fails
python tools/build_site.py vendor/codemirror-5.65.16.min.css      # -> site/index.html
```

`tools/grade.mjs` (add `--pch` to use the C++ precompiled header like the browser) uses the same compiler, flags and runtime as the site. Get the compiler with
`npm pack @yowasp/clang@22.0.0-git20542-10` and unpack it; `<path>/gen/bundle.js` is inside.
`tools/make_pch.mjs` rebuilds the precompiled header and `tools/package.py <path>/gen` re-packs
the compiler files into `site/cc/`.

## Licences

See [THIRD_PARTY.md](THIRD_PARTY.md). The compiler files in `site/cc/` are from LLVM (Apache
License 2.0 with LLVM Exceptions), packaged by YoWASP.
