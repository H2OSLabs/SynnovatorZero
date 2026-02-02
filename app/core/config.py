"""Application configuration settings.

Environment variables:
- MOCK_AUTH: Enable mock authentication for development (default: true)
- MOCK_USER_ID: Default user ID in mock mode (default: 1)
- MOCK_USER_ROLE: Default user role in mock mode (default: participant)
- DATABASE_URL: Database connection URL (default: sqlite:///./data/synnovator.db)
"""
from typing import Literal
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # 忽略未定义的环境变量
    )

    # Authentication
    mock_auth: bool = True
    mock_user_id: int = 1
    mock_user_role: Literal["participant", "organizer", "admin"] = "participant"

    # Database
    database_url: str = "sqlite:///./data/synnovator.db"

    # API
    api_prefix: str = "/api"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
