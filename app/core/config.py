"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object for the application."""

    DATABASE_URL: str = "sqlite:///./ecommerce_intelligence.db"
    SECRET_KEY: str = "changeme-super-secret-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
