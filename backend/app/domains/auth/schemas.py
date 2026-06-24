from pydantic import BaseModel


class AuthStatus(BaseModel):
    oauth_configured: bool
    allowed_email_configured: bool
