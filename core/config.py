from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class AppConfig:
    env: str = "development"
    debug: bool = False
    model_path: str = "models/your-model.gguf"
    model_context_size: int = 4096
    max_tokens: int = 512
    db_path: str = "data/reign.db"
    host: str = "0.0.0.0"
    port: int = 8000
    api_base_url: str = "http://localhost:8000"
    master_name: str = "MASTER"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    env: str = "development"
    debug: bool = False
    reign_model_path: str = "models/your-model.gguf"
    reign_model_context_size: int = 4096
    reign_max_tokens: int = 512
    reign_db_path: str = "data/reign.db"
    reign_host: str = "0.0.0.0"
    reign_port: int = 8000
    reign_api_base_url: str = "http://localhost:8000"
    reign_master_name: str = "MASTER"

    @property
    def config(self) -> AppConfig:
        return AppConfig(
            env=self.env,
            debug=self.debug,
            model_path=self.reign_model_path,
            model_context_size=self.reign_model_context_size,
            max_tokens=self.reign_max_tokens,
            db_path=self.reign_db_path,
            host=self.reign_host,
            port=self.reign_port,
            api_base_url=self.reign_api_base_url,
            master_name=self.reign_master_name,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
