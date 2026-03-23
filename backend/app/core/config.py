from pydantic import EmailStr, AnyUrl, model_validator
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        extra="ignore",
        env_file=".env"
    )

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{
            self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    origins: Annotated[list[AnyUrl] | str, "This are list of origins"] = []

    SECRET_KEY: str
    # (60 * 24 * 8) minutes = 8 days
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60 * 24 * 8
    EMAIL_TEST_USER: EmailStr = "test@example.com"

    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None
    FRONTEND_HOST: str = "http://localhost:5173"

    @model_validator(mode="after")
    def _set_default_emails_from(self):
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)


settings = Settings()
