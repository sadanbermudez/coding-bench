import json
import sys
from collections import defaultdict


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    try:
        lines = open(args[0], encoding="utf-8").read().splitlines()
    except OSError as e:
        print(f"cannot read {args[0]}: {e}", file=sys.stderr)
        return 1
    rows, bad = [], 0
    for line in lines:
        try:
            rows.append(json.loads(line))
        except ValueError:
            bad += 1
    if bad:
        print(f"skipped {bad} bad lines", file=sys.stderr)
    by = defaultdict(list)
    for r in rows:
        by[r["name"]].append(r["seconds"])
    ok = sum(r["status"] == "ok" for r in rows)
    if as_json:
        print(json.dumps({"runs": len(rows), "ok": ok, "failed": len(rows) - ok, "by_name": {
            n: {"runs": len(by[n]), "avg_seconds": round(sum(by[n]) / len(by[n]), 1)} for n in sorted(by)}}))
        return 0
    print(f"{len(rows)} runs, {ok} ok, {len(rows) - ok} failed")
    for name in sorted(by):
        print(f"  {name}: {len(by[name])} runs, avg {sum(by[name]) / len(by[name]):.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
