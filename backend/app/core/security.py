def is_allowed_google_email(email: str, allowed_email: str) -> bool:
    return bool(email) and bool(allowed_email) and email.lower() == allowed_email.lower()
