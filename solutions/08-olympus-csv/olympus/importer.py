import csv
import io
from datetime import date


def load_sets(text):
    text = text.lstrip("\ufeff")
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return []
    sep = ";" if ";" in lines[0] else ","
    rows = []
    for r in csv.DictReader(io.StringIO("\n".join(lines)), delimiter=sep):
        w = r["weight_kg"].strip()
        if sep == ";":
            w = w.replace(",", ".")
        rows.append({"date": date.fromisoformat(r["date"].strip()), "exercise": r["exercise"].strip(),
                     "reps": int(r["reps"]), "weight_kg": float(w)})
    return rows
