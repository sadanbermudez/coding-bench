import json
import os


def brief_header():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    return f"Brief ({cfg['timezone']})"
