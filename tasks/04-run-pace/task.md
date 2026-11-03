Create `pace.py` with:
- `parse_time(s) -> int`: seconds from "H:MM:SS", "MM:SS" or "SS". Raise ValueError for anything else (empty, negative, letters, more than three fields, or a minutes/seconds field >= 60 when a larger field precedes it).
- `pace_per_km(time_str, km) -> str`: pace as "M:SS/km", rounded to the nearest whole second (half rounds up). Raise ValueError if km <= 0.
- `finish_time(pace_str, km) -> str`: the inverse; pace like "4:59/km" (the "/km" is optional) times km, rounded to the nearest second, formatted "H:MM:SS".
