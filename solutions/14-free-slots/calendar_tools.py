from datetime import timedelta


def free_slots(calendars, day_start, day_end, min_minutes):
    busy = sorted((max(s, day_start), min(e, day_end)) for c in calendars for s, e in c
                  if e > s and e > day_start and s < day_end)
    out, cur = [], day_start
    need = timedelta(minutes=min_minutes)
    for s, e in busy:
        if s - cur >= need:
            out.append((cur, s))
        cur = max(cur, e)
    if day_end - cur >= need:
        out.append((cur, day_end))
    return out
