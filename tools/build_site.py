"""Builds the page from src/index.template.html, the CodeMirror stylesheet and build/problems.json.
Writes two versions:
  site/index.html      complete standalone page (GitHub Pages, any static web server)
  build/artifact.html  body-only version for the claude.ai artifact (the host adds <html>/<head>)
usage: python tools/build_site.py <codemirror.min.css>"""
import os, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
tpl = open(os.path.join(root, "src", "index.template.html"), encoding="utf-8").read()
css = open(sys.argv[1], encoding="utf-8").read()
data = open(os.path.join(root, "build", "problems.json"), encoding="utf-8").read()
data = data.replace("</", "<\\/")          # keep "</script>" from ending the data block
for k in ("/*__CMCSS__*/", "/*__DATA__*/"):
    assert tpl.count(k) == 1, k
body = tpl.replace("/*__CMCSS__*/", css).replace("/*__DATA__*/", data)

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
standalone = head + body + "\n</body>\n</html>\n"

open(os.path.join(root, "site", "index.html"), "w", encoding="utf-8").write(standalone)
open(os.path.join(root, "build", "artifact.html"), "w", encoding="utf-8").write(body)
print("site/index.html", len(standalone.encode()), "bytes; build/artifact.html", len(body.encode()), "bytes")
