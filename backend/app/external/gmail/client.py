class GmailSmtpClient:
    def send_alert(self, recipient: str, subject: str, body: str) -> None:
        raise NotImplementedError("Gmail SMTP 계정 설정 후 구현")
