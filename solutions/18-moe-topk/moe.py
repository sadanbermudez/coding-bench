import math


def route(logits, k):
    if k < 1 or k > len(logits):
        raise ValueError(k)
    top = sorted(range(len(logits)), key=lambda i: (-logits[i], i))[:k]
    m = max(logits[i] for i in top)
    ex = {i: math.exp(logits[i] - m) for i in top}
    z = sum(ex.values())
    return sorted(((i, ex[i] / z) for i in top), key=lambda p: (-p[1], p[0]))


def route_batch(batch, k, capacity):
    load, out = {}, []
    for logits in batch:
        kept = []
        for i, w in route(logits, k):
            if load.get(i, 0) < capacity:
                load[i] = load.get(i, 0) + 1
                kept.append((i, w))
        z = sum(w for _, w in kept)
        out.append([(i, w / z) for i, w in kept])
    return out
