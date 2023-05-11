from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from decouple import config


class Settings(BaseSettings):
    API_STR: str = "/api"
    MAPS_API_KEY: str = config("MAPS_API_KEY", cast=str)
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_TITLE: str = "Python Backend"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        # Add your frontend url here
        # "http://localhost:3000"
    ]

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    PROD_DB: str = config("PROD_DB", cast=str)
    TEST_DB: str = config("TEST_DB", cast=str)

    # Testing
    TESTING: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
