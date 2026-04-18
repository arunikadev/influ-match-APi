import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str = "influMatch_super_secret_key_2024_GANTI_DI_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 hari

    # Database: Gunakan /tmp di Vercel krn selain itu read-only, kalau lokal pakai direktori saat ini
    DATABASE_URL: str = "sqlite:////tmp/influmatch.db" if os.environ.get("VERCEL") else "sqlite:///./influmatch.db"

    # App
    APP_NAME: str = "InfluMatch API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
