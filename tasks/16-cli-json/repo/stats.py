import json
import sys
from collections import defaultdict


def main(argv):
    path = argv[0]
    rows = [json.loads(line) for line in open(path, encoding="utf-8")]
    by = defaultdict(list)
    for r in rows:
        by[r["name"]].append(r["seconds"])
    ok = sum(r["status"] == "ok" for r in rows)
    print(f"{len(rows)} runs, {ok} ok, {len(rows) - ok} failed")
    for name in sorted(by):
        print(f"  {name}: {len(by[name])} runs, avg {sum(by[name]) / len(by[name]):.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
