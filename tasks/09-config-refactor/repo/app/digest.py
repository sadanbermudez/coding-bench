import json
import os

DEFAULTS = {"timezone": "Europe/Madrid", "max_items": 10}


def _config():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    with open(path, encoding="utf-8") as f:
        return {**DEFAULTS, **json.load(f)}


def digest(items):
    cfg = _config()
    return items[: cfg["max_items"]]
