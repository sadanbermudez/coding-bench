KG_PER_LB = 0.45359237


def lb_to_kg(lb: float) -> float:
    return round(lb / KG_PER_LB, 2)


def kg_to_lb(kg: float) -> float:
    return round(kg * KG_PER_LB, 2)


def km_to_miles(km: float) -> float:
    return round(km / 1.609344, 3)
