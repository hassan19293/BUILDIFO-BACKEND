import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Buildifo CRM Backend"
    environment: str = "development"
    database_url: str = os.environ.get("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/buildifo")
    cors_origins: str = "https://buildifo.com,https://www.buildifo.com,http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()