import csv
import io
from datetime import date


def load_sets(text: str) -> list[dict]:
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        rows.append({
            "date": date.fromisoformat(r["date"]),
            "exercise": r["exercise"].strip(),
            "reps": int(r["reps"]),
            "weight_kg": float(r["weight_kg"]),
        })
    return rows
