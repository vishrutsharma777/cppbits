"""Packs the compiler for the website: gzip the big files, split them into chunks below the
15 MB per-file limit, copy the small files, and write site/cc/manifest.json.
usage: python tools/package.py <path to @yowasp/clang package/gen>"""
import gzip, json, os, shutil, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
gen = sys.argv[1]
cc = os.path.join(root, "site", "cc")
CHUNK = 14 * 1000 * 1000

def pack(src, name, mime):
    data = open(src, "rb").read()
    gz = gzip.compress(data, 9)
    parts = []
    for i in range(0, len(gz), CHUNK):
        pname = f"{name}.gz{len(parts)}.wasm"   # .wasm is a type the host serves; the bytes are gzip
        open(os.path.join(cc, pname), "wb").write(gz[i:i + CHUNK])
        parts.append(pname)
    print(f"{name}: {len(data):,} -> {len(gz):,} bytes gz, {len(parts)} part(s)")
    return parts

files, sizes = {}, {}
for src, name, mime in [(os.path.join(gen, "llvm.core.wasm"), "llvm.core.wasm", "application/wasm"),
                        (os.path.join(gen, "llvm-resources.tar"), "llvm-resources.tar", "application/octet-stream"),
                        (os.path.join(root, "build", "pre.hpp.pch"), "pre.hpp.pch", "application/octet-stream")]:
    parts = pack(src, name, mime)
    files[name] = {"parts": parts, "type": mime}
    for p in parts:
        sizes[p] = os.path.getsize(os.path.join(cc, p))
for f in ["bundle.js", "llvm.core2.wasm", "llvm.core3.wasm", "llvm.core4.wasm"]:
    shutil.copy(os.path.join(gen, f), os.path.join(cc, f))
json.dump({"files": files, "sizes": sizes}, open(os.path.join(cc, "manifest.json"), "w"), indent=1)
total = sum(os.path.getsize(os.path.join(cc, f)) for f in os.listdir(cc))
print(f"site/cc total {total:,} bytes in {len(os.listdir(cc))} files")
