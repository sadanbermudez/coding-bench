def twr(valuations, flows):
    if len(valuations) < 2:
        raise ValueError("need two valuations")
    g = 1.0
    for (d0, v0), (d1, v1) in zip(valuations, valuations[1:]):
        if v0 == 0:
            raise ValueError("zero start")
        f = sum(a for d, a in flows if d0 < d <= d1)
        g *= (v1 - f) / v0
    return g - 1
