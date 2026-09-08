import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Smart Attendance API")
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name: str = os.getenv("DB_NAME", "smart_attendance")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    cv_mode: str = os.getenv("CV_MODE", "mock")
    camera_fps: int = int(os.getenv("CAMERA_FPS", "10"))
    attendance_cooldown_seconds: float = float(os.getenv("ATTENDANCE_COOLDOWN_SECONDS", "30"))


@lru_cache
def get_settings() -> Settings:
    return Settings()