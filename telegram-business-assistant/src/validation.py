"""Small, independently testable validators for user-provided lead data."""

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^\+?[0-9\s().-]{7,25}$")


def validate_contact(value: str) -> bool:
    """Accept a plausible email address or phone number."""
    normalized = value.strip()
    if not normalized or len(normalized) > 120:
        return False
    return bool(_EMAIL_RE.fullmatch(normalized) or _PHONE_RE.fullmatch(normalized))


def validate_details(value: str) -> tuple[bool, str]:
    """Return a validation result and a user-facing explanation."""
    normalized = value.strip()
    if len(normalized) < 10:
        return False, "Добавьте немного деталей — от 10 символов."
    if len(normalized) > 1000:
        return False, "Сообщение слишком длинное. Ограничение — 1000 символов."
    return True, ""
