import math
import re


def parse_time(s):
    if not re.fullmatch(r"\d+(:\d+){0,2}", s or ""):
        raise ValueError(s)
    parts = [int(p) for p in s.split(":")]
    if any(p >= 60 for p in parts[1:]):
        raise ValueError(s)
    t = 0
    for p in parts:
        t = t * 60 + p
    return t


def _r(x):
    return int(math.floor(x + 0.5))


def pace_per_km(time_str, km):
    if km <= 0:
        raise ValueError(km)
    s = _r(parse_time(time_str) / km)
    return f"{s // 60}:{s % 60:02d}/km"


def finish_time(pace_str, km):
    s = _r(parse_time(pace_str.removesuffix("/km")) * km)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}"
