from pydantic import BaseModel


class GmailMessage(BaseModel):
    recipient: str
    subject: str
    body: str
