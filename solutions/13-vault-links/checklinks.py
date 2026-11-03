import os
import re
from pathlib import Path
from urllib.parse import unquote

WIKI = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
MD = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


def broken_links(root):
    root = Path(root)
    files = sorted(root.rglob("*.md"))
    names = {p.stem.lower() for p in files}
    out = set()
    for p in files:
        text = re.sub(r"```.*?```", "", p.read_text(encoding="utf-8"), flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        rel = p.relative_to(root).as_posix()
        for t in WIKI.findall(text):
            if t.strip().lower() not in names:
                out.add((rel, t))
        for t in MD.findall(text):
            if t.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(t.split("#")[0])
            if not (p.parent / target).exists():
                out.add((rel, t))
    return sorted(out)
