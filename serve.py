"""Serve the site locally:  python serve.py   then open http://localhost:8000
(Opening site/index.html as a file does not work: browsers only start the compiler's module
workers from http:// or https:// pages.)"""
import functools, http.server, mimetypes, os, sys

# Windows can map .js to text/plain via the registry, which breaks module scripts
for ext, mime in {".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm",
                  ".json": "application/json", ".html": "text/html", ".hpp": "text/plain"}.items():
    mimetypes.add_type(mime, ext)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
site = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site)
handler.func.extensions_map.update({".js": "text/javascript", ".wasm": "application/wasm"})
print(f"CppBits on http://localhost:{port}  (Ctrl+C to stop)")
http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
