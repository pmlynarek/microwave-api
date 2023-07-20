from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    PROJECT_NAME: str = "Microwave"
    SECRET_KEY: str = "secret"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOWED_HOSTS: List[str] = ["*"]

    REDIS_URL: str = "redis://localhost"


settings = Settings()
