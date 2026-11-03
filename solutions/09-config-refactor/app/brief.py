from app.config import load_config


def brief_header():
    return f"Brief ({load_config()['timezone']})"
