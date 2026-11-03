import re

EMAIL = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[A-Z0-9]{11,30}|(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?)\b")
PHONE = re.compile(r"\+\d[\d -]{7,}\d")


def _phone(text):
    for m in PHONE.finditer(text):
        s = m.group(0)
        if "  " in s or "--" in s:
            continue
        n = sum(c.isdigit() for c in s)
        if 9 <= n <= 15:
            return True
    return False


def _iban(text):
    for m in IBAN.finditer(text):
        n = len(m.group(0).replace(" ", ""))
        if 15 <= n <= 34:
            return True
    return False


def find_private(text):
    kinds = []
    if EMAIL.search(text): kinds.append("email")
    if _iban(text): kinds.append("iban")
    if _phone(text): kinds.append("phone")
    return kinds


def is_private(text):
    return bool(find_private(text))
