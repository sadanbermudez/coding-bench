from pathlib import Path

from notes.models import Note
from notes.text import slugify  # noqa: F401  (still importable from here)


def load_folder(folder):
    out = []
    for p in sorted(Path(folder).glob("*.md")):
        lines = p.read_text(encoding="utf-8").splitlines()
        title = lines[0].lstrip("# ").strip()
        tags = [t.strip() for t in lines[1].removeprefix("tags:").split(",") if t.strip()]
        out.append(Note(title=title, tags=tags, body="\n".join(lines[2:])))
    return out
