def expected_score(me: float, opp: float) -> float:
    return 1 / (1 + 10 ** ((me - opp) / 400))


def update(me: float, opp: float, score: float, k: float = 20) -> float:
    exp = expected_score(opp, me)
    return round(me + k * (exp - score), 1)
