import re

EMAIL = re.compile(r"\b[a-z]+@[a-z]+\.[a-z]{2,}\b")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
PHONE = re.compile(r"\+\d{9,15}")


def find_private(text: str) -> list[str]:
    kinds = []
    if EMAIL.search(text):
        kinds.append("email")
    if IBAN.search(text):
        kinds.append("iban")
    if PHONE.search(text):
        kinds.append("phone")
    return kinds


def is_private(text: str) -> bool:
    return bool(find_private(text))
