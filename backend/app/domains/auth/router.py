from fastapi import APIRouter

from app.common.responses import ok
from app.domains.auth.service import get_auth_status

router = APIRouter()


@router.get("/status")
def status():
    return ok(get_auth_status())


@router.get("/google/login")
def google_login_placeholder():
    return ok({"implemented": False}, "Google OAuth 설정 후 연결 예정")
