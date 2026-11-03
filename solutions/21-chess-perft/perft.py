KN = (-21, -19, -12, -8, 8, 12, 19, 21)
KG = (-11, -10, -9, -1, 1, 9, 10, 11)
BI = (-11, -9, 9, 11)
RO = (-10, -1, 1, 10)


def sq(n):
    return 21 + (8 - int(n[1])) * 10 + ord(n[0]) - 97


def name(i):
    return chr(97 + (i - 21) % 10) + str(8 - (i - 21) // 10)


def parse(fen):
    p = fen.split()
    b = ["#"] * 120
    for r, row in enumerate(p[0].split("/")):
        f = 0
        for ch in row:
            if ch.isdigit():
                for _ in range(int(ch)):
                    b[21 + r * 10 + f] = "."; f += 1
            else:
                b[21 + r * 10 + f] = ch; f += 1
    return b, p[1], "" if p[2] == "-" else p[2], None if p[3] == "-" else sq(p[3])


def attacked(b, s, by_white):
    if by_white:
        if b[s + 9] == "P" or b[s + 11] == "P":
            return True
        n, k, bq, rq = "N", "K", "BQ", "RQ"
    else:
        if b[s - 9] == "p" or b[s - 11] == "p":
            return True
        n, k, bq, rq = "n", "k", "bq", "rq"
    for d in KN:
        if b[s + d] == n:
            return True
    for d in KG:
        if b[s + d] == k:
            return True
    for d in BI:
        t = s + d
        while b[t] == ".":
            t += d
        if b[t] in bq:
            return True
    for d in RO:
        t = s + d
        while b[t] == ".":
            t += d
        if b[t] in rq:
            return True
    return False


def enemy(q, w):
    return q not in ".#" and q.isupper() != w


def gen(st):
    b, side, cas, ep = st
    w = side == "w"
    out = []
    for s in range(21, 99):
        p = b[s]
        if p in ".#" or p.isupper() != w:
            continue
        u = p.upper()
        if u == "P":
            fwd = -10 if w else 10
            start_row, promo_row = (8, 2) if w else (3, 9)

            def add(t):
                if t // 10 == promo_row:
                    out.extend((s, t, x) for x in "qrbn")
                else:
                    out.append((s, t, None))
            t = s + fwd
            if b[t] == ".":
                add(t)
                if s // 10 == start_row and b[t + fwd] == ".":
                    out.append((s, t + fwd, None))
            for d in (fwd - 1, fwd + 1):
                t = s + d
                if enemy(b[t], w):
                    add(t)
                elif t == ep and b[t] == ".":
                    out.append((s, t, "ep"))
        elif u in "NK":
            for d in (KN if u == "N" else KG):
                t = s + d
                if b[t] == "." or enemy(b[t], w):
                    out.append((s, t, None))
            if u == "K":
                home, r = (95, "R") if w else (25, "r")
                ks, qs = ("K", "Q") if w else ("k", "q")
                if s == home and not attacked(b, s, not w):
                    if ks in cas and b[s + 1] == b[s + 2] == "." and b[s + 3] == r \
                            and not attacked(b, s + 1, not w) and not attacked(b, s + 2, not w):
                        out.append((s, s + 2, "castle"))
                    if qs in cas and b[s - 1] == b[s - 2] == b[s - 3] == "." and b[s - 4] == r \
                            and not attacked(b, s - 1, not w) and not attacked(b, s - 2, not w):
                        out.append((s, s - 2, "castle"))
        else:
            dirs = BI if u == "B" else RO if u == "R" else BI + RO
            for d in dirs:
                t = s + d
                while b[t] == ".":
                    out.append((s, t, None)); t += d
                if enemy(b[t], w):
                    out.append((s, t, None))
    return out


def make(st, m):
    b, side, cas, ep = st
    b = b[:]
    s, t, x = m
    p = b[s]
    w = side == "w"
    b[t] = p; b[s] = "."
    if x == "ep":
        b[t + (10 if w else -10)] = "."
    elif x == "castle":
        rf, rt = (t + 1, t - 1) if t > s else (t - 2, t + 1)
        b[rt] = b[rf]; b[rf] = "."
    elif x:
        b[t] = x.upper() if w else x
    nep = (s + t) // 2 if p in "Pp" and abs(t - s) == 20 else None
    for corner, rights in ((95, "KQ"), (25, "kq"), (98, "K"), (91, "Q"), (28, "k"), (21, "q")):
        if s == corner or t == corner:
            cas = "".join(c for c in cas if c not in rights)
    return b, "b" if w else "w", cas, nep


def legal(st):
    w = st[1] == "w"
    res = []
    for m in gen(st):
        ns = make(st, m)
        if not attacked(ns[0], ns[0].index("K" if w else "k"), not w):
            res.append((m, ns))
    return res


def perft(fen, depth):
    def rec(st, d):
        if d == 0:
            return 1
        ms = legal(st)
        if d == 1:
            return len(ms)
        return sum(rec(ns, d - 1) for _, ns in ms)
    return rec(parse(fen), depth)


def legal_moves(fen):
    return sorted(name(s) + name(t) + (x if x in ("q", "r", "b", "n") else "")
                  for (s, t, x), _ in legal(parse(fen)))
