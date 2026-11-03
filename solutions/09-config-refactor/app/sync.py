from app.config import load_config


def batch_size():
    return load_config()["max_items"] * 2
