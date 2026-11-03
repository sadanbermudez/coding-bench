def expected_score(me, opp):
    return 1 / (1 + 10 ** ((opp - me) / 400))


def update(me, opp, score, k=20):
    return round(me + k * (score - expected_score(me, opp)), 1)
