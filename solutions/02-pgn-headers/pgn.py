import re

TAG = re.compile(r'^\[(\w+)\s+"((?:[^"\\]|\\.)*)"\]\s*$')


def parse_headers(pgn):
    games, cur, in_comment = [], {}, False
    for line in pgn.splitlines():
        s = line.strip()
        m = TAG.match(s) if not in_comment else None
        if m:
            cur[m.group(1)] = re.sub(r"\\(.)", r"\1", m.group(2))
            continue
        if s and cur:
            games.append(cur); cur = {}
        for ch in s:
            if ch == "{": in_comment = True
            elif ch == "}": in_comment = False
    if cur:
        games.append(cur)
    return games
