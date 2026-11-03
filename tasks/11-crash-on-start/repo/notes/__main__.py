import sys

from notes.storage import load_folder


def main(argv):
    if len(argv) != 2 or argv[0] != "stats":
        print("usage: python -m notes stats <folder>")
        return 2
    notes = load_folder(argv[1])
    words = sum(len(n.body.split()) for n in notes)
    tags = sorted({t for n in notes for t in n.tags})
    print(f"{len(notes)} notes, {words} words, tags: {', '.join(tags)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
