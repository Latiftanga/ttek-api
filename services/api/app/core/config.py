from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    ENVIRONMENT: str = "development"
    SECRET_KEY: str
    ALLOWED_ORIGINS: str = "http://localhost"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24        # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str
    REDIS_PASSWORD: str = ""

    # CouchDB
    COUCHDB_URL: str
    COUCHDB_USER: str
    COUCHDB_PASSWORD: str

    # MinIO
    MINIO_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str

    # Frontend
    NEXT_PUBLIC_API_URL: str = ""
    NEXT_PUBLIC_APP_NAME: str = "Ghana SIS"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
