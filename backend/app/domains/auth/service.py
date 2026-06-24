from app.core.config import settings


def get_auth_status() -> dict:
    return {
        "oauth_configured": bool(settings.google_client_id and settings.google_client_secret),
        "allowed_email_configured": bool(settings.google_allowed_email),
    }
