from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CATCH_",
        env_file=".env",
        extra="ignore",
    )

    env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    secret_key: str = "change-me-in-production"
    allowed_origins: str = "http://localhost:19006"
    api_key: str = "dev-api-key"

    yolo_weights: str = "app/ml/weights/yolov8n.pt"
    yolo_device: str = "cpu"
    max_upload_mb: int = 8

    scrape_user_agent: str = "CATCH-Bot/0.1"
    scrape_timeout_seconds: int = 12

    @property
    def origin_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def weights_path(self) -> Path:
        return Path(self.yolo_weights)


@lru_cache
def get_settings() -> Settings:
    return Settings()
