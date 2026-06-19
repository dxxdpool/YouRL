import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    URL_CREATION_RATE_LIMIT: int = 5
    URL_CREATION_RATE_WINDOW_SECONDS: int = 60
    ALLOW_REGISTRATION: bool = True

    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        extra="ignore",
    )


settings = Settings()
