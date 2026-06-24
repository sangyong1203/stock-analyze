from email.message import EmailMessage
import smtplib

from app.external.gmail.types import GmailMessage


class GmailSmtpClient:
    def __init__(self, host: str, port: int, username: str, app_password: str, timeout: int = 20) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.app_password = app_password
        self.timeout = timeout

    def send(self, message: GmailMessage) -> None:
        email = EmailMessage()
        email["From"] = self.username
        email["To"] = message.recipient
        email["Subject"] = message.subject
        email.set_content(message.body, charset="utf-8")

        with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.app_password)
            smtp.send_message(email)
