from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.auth.service import (
    build_frontend_dashboard_url,
    build_google_login_url,
    create_google_oauth_state,
    exchange_google_code,
    fetch_google_userinfo,
    get_auth_status,
    upsert_google_user,
    validate_google_userinfo,
)

router = APIRouter()


@router.get("/status")
def status():
    return ok(get_auth_status())


@router.get("/google/login")
def google_login(request: Request):
    auth_status = get_auth_status()
    if not auth_status["oauth_configured"] or not auth_status["allowed_email_configured"]:
        raise HTTPException(status_code=400, detail="Google OAuth is not fully configured")
    state = create_google_oauth_state()
    response = RedirectResponse(build_google_login_url(request, state), status_code=302)
    response.set_cookie(
        key="google_oauth_state",
        value=state,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=600,
    )
    return response


@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    expected_state = request.cookies.get("google_oauth_state")
    if not expected_state or expected_state != state:
        raise HTTPException(status_code=400, detail="Invalid Google OAuth state")

    token_response = await exchange_google_code(request, code)
    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(status_code=502, detail="Google access token missing")

    userinfo = await fetch_google_userinfo(access_token)
    email, name, google_sub = validate_google_userinfo(userinfo)
    upsert_google_user(
        db,
        email=email,
        name=name,
        google_sub=google_sub,
        avatar_url=userinfo.get("picture"),
    )

    response = RedirectResponse(f"{build_frontend_dashboard_url()}?auth=success", status_code=302)
    response.delete_cookie("google_oauth_state")
    return response
