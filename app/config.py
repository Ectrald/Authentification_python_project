import secrets
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    database_url: PostgresDsn

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""

    frontend_url: str = "http://localhost:3000"
    token_expire_minutes: int = 1440

    jwt_secret_key: str = secrets.token_urlsafe(48)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
