from collections import defaultdict


def near_duplicates(fps):
    if not fps:
        return []
    pairs = set()
    for pos in range(len(fps[0])):
        groups = defaultdict(list)
        for i, f in enumerate(fps):
            groups[f[:pos] + f[pos + 1:]].append(i)
        for idx in groups.values():
            if len(idx) > 1:
                for a in range(len(idx)):
                    for b in range(a + 1, len(idx)):
                        pairs.add((idx[a], idx[b]))
    return sorted(pairs)
