import sys


class P:
    def __init__(self, s):
        self.s, self.i = s, 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None

    def take(self):
        c = self.peek(); self.i += 1; return c


def parse(s):
    p = P(s)
    if s == "":
        return ("empty",)
    node = alt(p)
    if p.peek() is not None:
        raise ValueError(f"unexpected {p.peek()!r} at {p.i}")
    return node


def alt(p):
    node = cat(p)
    while p.peek() == "|":
        p.take()
        node = ("alt", node, cat(p))
    return node


def cat(p):
    parts = []
    while p.peek() not in (None, "|", ")"):
        parts.append(rep(p))
    if not parts:
        raise ValueError("empty expression")
    node = parts[0]
    for x in parts[1:]:
        node = ("cat", node, x)
    return node


def rep(p):
    a = atom(p)
    if p.peek() in ("*", "+", "?"):
        a = ({"*": "star", "+": "plus", "?": "opt"}[p.take()], a)
        if p.peek() in ("*", "+", "?"):
            raise ValueError("stacked quantifier")
    return a


def atom(p):
    c = p.take()
    if c is None or c in "*+?|)":
        raise ValueError(f"nothing to repeat / unexpected {c!r}")
    if c == "(":
        node = alt(p)
        if p.take() != ")":
            raise ValueError("unbalanced (")
        return node
    if c == "[":
        neg = p.peek() == "^"
        if neg:
            p.take()
        items = []
        while True:
            ch = p.take()
            if ch is None:
                raise ValueError("unterminated class")
            if ch == "]" and items:
                break
            if ch == "\\":
                ch = p.take()
                if ch is None:
                    raise ValueError("trailing backslash")
            if p.peek() == "-" and p.i + 1 < len(p.s) and p.s[p.i + 1] != "]":
                p.take(); hi = p.take()
                items.append((ch, hi))
            else:
                items.append((ch, ch))
        return ("set", tuple(items), neg)
    if c == ".":
        return ("any",)
    if c == "\\":
        c = p.take()
        if c is None:
            raise ValueError("trailing backslash")
    return ("lit", c)


def fullmatch(pattern, text):
    tree = parse(pattern)
    n = len(text)
    memo = {}
    sys.setrecursionlimit(10000)

    def ends(node, i):
        key = (id(node), i)
        if key in memo:
            return memo[key]
        k = node[0]
        if k == "empty":
            r = frozenset([i])
        elif k in ("lit", "any", "set"):
            ok = i < n and (k == "any" or (k == "lit" and text[i] == node[1]) or
                            (k == "set" and any(lo <= text[i] <= hi for lo, hi in node[1]) != node[2]))
            r = frozenset([i + 1]) if ok else frozenset()
        elif k == "cat":
            r = frozenset(j for m in ends(node[1], i) for j in ends(node[2], m))
        elif k == "alt":
            r = ends(node[1], i) | ends(node[2], i)
        elif k == "opt":
            r = ends(node[1], i) | {i}
        else:  # star / plus
            seen, todo = set(), [i]
            first = set(ends(node[1], i))
            if k == "star":
                seen.add(i)
            seen |= first; todo = list(first)
            while todo:
                m = todo.pop()
                for j in ends(node[1], m):
                    if j not in seen:
                        seen.add(j); todo.append(j)
            r = frozenset(seen)
        memo[key] = r
        return r

    return n in ends(tree, 0)
