from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Stock Analyze"
    app_env: str = "local"
    database_url: str = "sqlite:///./stock_analyze.db"
    allowed_origin: str = "http://localhost:5173"
    google_client_id: str = ""
    google_client_secret: str = ""
    google_allowed_email: str = ""
    gmail_smtp_host: str = "smtp.gmail.com"
    gmail_smtp_port: int = 587
    gmail_smtp_username: str = ""
    gmail_smtp_app_password: str = ""
    alert_recipient_email: str = ""
    krx_api_base_url: str = "https://data-dbg.krx.co.kr/svc/apis"
    krx_auth_key: str = ""
    openai_api_key: str = ""
    openai_news_summary_model: str = ""
    openai_news_filter_model: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
