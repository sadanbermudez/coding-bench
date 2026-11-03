import re

TOK = re.compile(r"\s*(?:(\d+\.\d+|\d+)|('[^']*')|([A-Za-z_][A-Za-z_0-9]*)|(<=|>=|!=|<>|[=<>(),*]))")
AGGS = {"COUNT", "SUM", "AVG", "MIN", "MAX"}


def tokenize(s):
    out, pos, s = [], 0, s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError(f"bad token at {pos}")
        num, st, ident, op = m.groups()
        if num:
            out.append(("num", float(num) if "." in num else int(num)))
        elif st:
            out.append(("str", st[1:-1]))
        elif ident:
            out.append(("id", ident))
        else:
            out.append(("op", op))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    return out


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self):
        tok = self.peek()
        if tok[0] is None:
            raise ValueError("unexpected end")
        self.i += 1
        return tok

    def is_kw(self, kw):
        k, v = self.peek()
        return k == "id" and v.upper() == kw

    def kw(self, kw):
        if not self.is_kw(kw):
            raise ValueError(f"expected {kw}")
        self.i += 1

    def op(self, o):
        if self.peek() != ("op", o):
            raise ValueError(f"expected {o}")
        self.i += 1

    def ident(self):
        k, v = self.take()
        if k != "id":
            raise ValueError("expected name")
        return v

    def item(self):
        k, v = self.peek()
        if k == "id" and v.upper() in AGGS and self.t[self.i + 1:self.i + 2] == [("op", "(")]:
            self.i += 2
            if self.peek() == ("op", "*"):
                if v.upper() != "COUNT":
                    raise ValueError("only COUNT(*)")
                self.i += 1; col = "*"
            else:
                col = self.ident()
            self.op(")")
            return ("agg", v.upper(), col)
        return ("col", self.ident())

    def operand(self):
        k, v = self.take()
        if k == "id":
            return ("col", v)
        if k in ("num", "str"):
            return ("val", v)
        raise ValueError("bad operand")

    def cond(self):
        node = self.and_()
        while self.is_kw("OR"):
            self.i += 1; node = ("or", node, self.and_())
        return node

    def and_(self):
        node = self.not_()
        while self.is_kw("AND"):
            self.i += 1; node = ("and", node, self.not_())
        return node

    def not_(self):
        if self.is_kw("NOT"):
            self.i += 1
            return ("not", self.not_())
        if self.peek() == ("op", "("):
            self.i += 1; node = self.cond(); self.op(")")
            return node
        a = self.operand()
        k, o = self.take()
        if k != "op" or o not in ("=", "!=", "<>", "<", "<=", ">", ">="):
            raise ValueError("expected comparison")
        return ("cmp", o, a, self.operand())


def parse(sql):
    p = Parser(tokenize(sql))
    p.kw("SELECT")
    if p.peek() == ("op", "*"):
        p.i += 1; items = "*"
    else:
        items = [p.item()]
        while p.peek() == ("op", ","):
            p.i += 1; items.append(p.item())
    p.kw("FROM")
    q = {"items": items, "table": p.ident(), "where": None, "group": None, "order": [], "limit": None}
    if p.is_kw("WHERE"):
        p.i += 1; q["where"] = p.cond()
    if p.is_kw("GROUP"):
        p.i += 1; p.kw("BY"); q["group"] = p.ident()
    if p.is_kw("ORDER"):
        p.i += 1; p.kw("BY")
        while True:
            col, desc = p.ident(), False
            if p.is_kw("ASC"):
                p.i += 1
            elif p.is_kw("DESC"):
                p.i += 1; desc = True
            q["order"].append((col, desc))
            if p.peek() != ("op", ","):
                break
            p.i += 1
    if p.is_kw("LIMIT"):
        p.i += 1
        k, v = p.take()
        if k != "num" or not isinstance(v, int):
            raise ValueError("bad LIMIT")
        q["limit"] = v
    if p.peek()[0] is not None:
        raise ValueError(f"unexpected {p.peek()[1]!r}")
    return q


def rank(v):  # SQLite: numbers sort before text
    return (1, v) if isinstance(v, str) else (0, v)


def compare(o, a, b):
    if isinstance(a, str) != isinstance(b, str):
        a, b = rank(a), rank(b)
    return {"=": a == b, "!=": a != b, "<>": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[o]


def ev(node, row):
    k = node[0]
    if k == "or":
        return ev(node[1], row) or ev(node[2], row)
    if k == "and":
        return ev(node[1], row) and ev(node[2], row)
    if k == "not":
        return not ev(node[1], row)
    val = lambda x: row[x[1]] if x[0] == "col" else x[1]
    return compare(node[1], val(node[2]), val(node[3]))


def agg(name, col, rows):
    if name == "COUNT":
        return len(rows)
    vals = [r[col] for r in rows]
    if not vals:
        return None
    if name == "SUM":
        return sum(vals)
    if name == "AVG":
        return float(sum(vals)) / len(vals)
    return min(vals, key=rank) if name == "MIN" else max(vals, key=rank)


def sort(rows, order, get):
    for col, desc in reversed(order):
        rows.sort(key=lambda r: rank(get(r, col)), reverse=desc)
    return rows


def query(sql, tables):
    q = parse(sql)
    if q["table"] not in tables:
        raise ValueError(f"no table {q['table']}")
    rows = [r for r in tables[q["table"]] if q["where"] is None or ev(q["where"], r)]
    items = q["items"]
    has_agg = items != "*" and any(i[0] == "agg" for i in items)
    if q["group"]:
        groups = {}
        for r in rows:
            groups.setdefault(r[q["group"]], []).append(r)
        keys = sort(list(groups), q["order"], lambda k, c: k)
        out = [tuple(k if i[0] == "col" else agg(i[1], i[2], groups[k]) for i in items) for k in keys]
    elif has_agg:
        out = [tuple(agg(i[1], i[2], rows) if i[0] == "agg" else (rows[-1][i[1]] if rows else None) for i in items)]
    else:
        rows = sort(list(rows), q["order"], lambda r, c: r[c])
        cols = list(tables[q["table"]][0]) if items == "*" and tables[q["table"]] else \
            ([] if items == "*" else [i[1] for i in items])
        out = [tuple(r[c] for c in cols) for r in rows]
    return out[: q["limit"]] if q["limit"] is not None else out
