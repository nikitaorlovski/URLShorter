from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    DB_URL: str
    DEFAULT_LEN: int
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=ENV_PATH)


settings = Settings()
