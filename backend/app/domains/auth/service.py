from datetime import datetime
import json
from secrets import token_urlsafe
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request as UrlRequest, urlopen

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import is_allowed_google_email
from app.db.models import User
from app.domains.auth import repository


def get_auth_status() -> dict:
    return {
        "oauth_configured": bool(settings.google_client_id and settings.google_client_secret),
        "allowed_email_configured": bool(settings.google_allowed_email),
    }


def build_google_callback_url(request: Request) -> str:
    return str(request.url_for("google_callback"))


def build_frontend_dashboard_url() -> str:
    frontend_base_url = settings.allowed_origin or settings.allowed_origins.split(",")[0].strip()
    return f"{frontend_base_url.rstrip('/')}/dashboard"


def create_google_oauth_state() -> str:
    return token_urlsafe(32)


def build_google_login_url(request: Request, state: str) -> str:
    query = urlencode(
        {
            "client_id": settings.google_client_id,
            "redirect_uri": build_google_callback_url(request),
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "select_account",
        }
    )
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"


async def exchange_google_code(request: Request, code: str) -> dict:
    payload = urlencode(
        {
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": build_google_callback_url(request),
            "grant_type": "authorization_code",
        }
    ).encode()
    token_request = UrlRequest(
        "https://oauth2.googleapis.com/token",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(token_request, timeout=20) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Google token exchange failed")
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Google token exchange failed")
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid Google token response")


async def fetch_google_userinfo(access_token: str) -> dict:
    userinfo_request = UrlRequest(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET",
    )
    try:
        with urlopen(userinfo_request, timeout=20) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Google userinfo fetch failed")
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Google userinfo fetch failed")
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid Google userinfo response")


def validate_google_userinfo(userinfo: dict) -> tuple[str, str | None, str]:
    email = (userinfo.get("email") or "").strip()
    name = userinfo.get("name")
    google_sub = userinfo.get("sub")
    if not email or not google_sub:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google user info")
    if not is_allowed_google_email(email, settings.google_allowed_email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Google account is not allowed")
    return email, name, google_sub


def upsert_google_user(db: Session, email: str, name: str | None, google_sub: str, avatar_url: str | None) -> User:
    user = repository.get_user_by_google_sub(db, google_sub) or repository.get_user_by_email(db, email)
    if user is None:
        user = User(
            email=email,
            name=name,
            google_sub=google_sub,
            avatar_url=avatar_url,
            is_active=True,
            is_admin=True,
            last_login_at=datetime.utcnow(),
        )
    else:
        user.email = email
        user.name = name
        user.google_sub = google_sub
        user.avatar_url = avatar_url
        user.is_active = True
        user.last_login_at = datetime.utcnow()
    return repository.save_user(db, user)
