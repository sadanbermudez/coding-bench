from app.config import load_config


def digest(items):
    return items[: load_config()["max_items"]]
