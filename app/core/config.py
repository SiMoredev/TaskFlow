from pydantic_settings import BaseSettings
from typing import Optional
from app.db.session import DATABASE_URL

class Settings(BaseSettings):
    # === JWT ===
    SECRET_KEY: str = "your-super-secret-key-change-in-production"  # ⚠️ Замените в продакшене!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # === Database ===
    DATABASE_URL: str = DATABASE_URL

    # === CORS ===
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False

# Создаём экземпляр настроек
settings = Settings()