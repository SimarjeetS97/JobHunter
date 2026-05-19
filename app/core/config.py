from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "JobHunter API"
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/jobhunter")
    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-4.1-mini")
    openai_requests_per_minute: int = Field(default=60, ge=1)


@lru_cache
def get_settings() -> Settings:
    return Settings()
