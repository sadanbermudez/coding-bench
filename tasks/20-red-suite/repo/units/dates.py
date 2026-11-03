from datetime import date


def parse_eu(s: str) -> date:
    """Parse '02/11/2026' or '2-11-2026' (day first)."""
    sep = "/" if "/" in s else "-"
    d, m, y = s.split(sep)
    return date(int(y), int(d), int(m))


def week_label(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w}"
