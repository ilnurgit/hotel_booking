from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Django ---
    secret_key: str = Field(
        default="dev-secret-key",
        alias="DJANGO_SECRET_KEY",
    )
    debug: bool = Field(default=False, alias="DJANGO_DEBUG")
    allowed_hosts: str = Field(default="127.0.0.1,localhost", alias="DJANGO_ALLOWED_HOSTS")

    # --- Database ---
    db_name: str = Field(default="hotel_booking", alias="POSTGRES_DB")
    db_user: str = Field(default="hotel_booking", alias="POSTGRES_USER")
    db_password: str = Field(default="hotel_booking", alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="db", alias="POSTGRES_HOST")
    db_port: int = Field(default=5432, alias="POSTGRES_PORT")

    @property
    def allowed_hosts_list(self) -> list[str]:
        return [h.strip() for h in self.allowed_hosts.split(",") if h.strip()]


settings: AppSettings = AppSettings()  # type: ignore[call-arg]
