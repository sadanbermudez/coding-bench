from datetime import date


def parse_eu(s):
    sep = "/" if "/" in s else "-"
    d, m, y = s.split(sep)
    return date(int(y), int(m), int(d))


def week_label(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"
