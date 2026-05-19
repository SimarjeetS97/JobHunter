from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Job Hunter API"
    app_version: str = "0.1.0"
    environment: str = Field(default="development", alias="NODE_ENV")
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str
    redis_url: str
    openai_api_key: str = ""
    rate_limit_per_minute: int = 60


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
