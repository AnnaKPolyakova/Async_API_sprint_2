import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

from core.logger import LOGGING

load_dotenv()


logging_config.dictConfig(LOGGING)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PROTOCOL: str
    FILM_CACHE_EXPIRE_IN_SECONDS: int
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_PROTOCOL: str
    SIZE_FOR_LOAD_TO_ELASTICSEARCH: int
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    SIZE: int

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings().dict()