import json
import os

DEFAULTS = {"timezone": "Europe/Madrid", "max_items": 10}


def load_config(path=None):
    if path is None:
        path = os.environ.get("APP_CONFIG") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    with open(path, encoding="utf-8") as f:
        return {**DEFAULTS, **json.load(f)}
