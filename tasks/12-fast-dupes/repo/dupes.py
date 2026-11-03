def near_duplicates(fps: list[str]) -> list[tuple[int, int]]:
    out = []
    for i in range(len(fps)):
        for j in range(i + 1, len(fps)):
            a, b = fps[i], fps[j]
            if sum(x != y for x, y in zip(a, b)) <= 1:
                out.append((i, j))
    return out
