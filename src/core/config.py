import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from src.core.logger import LOGGING

load_dotenv()


logging_config.dictConfig(LOGGING)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="movies")
    REDIS_HOST: str = Field(env="REDIS_HOST", default="127.0.0.1")
    REDIS_PORT: int = Field(env="REDIS_PORT", default=6376)
    REDIS_PROTOCOL: str = Field(env="REDIS_PROTOCOL", default="redis")
    FILM_CACHE_EXPIRE_IN_SECONDS: int = Field(
        env="FILM_CACHE_EXPIRE_IN_SECONDS", default=350
    )
    ELASTIC_HOST: str = Field(env="ELASTIC_HOST", default="movies-elastic")
    ELASTIC_PORT: int = Field(env="ELASTIC_PORT", default=9200)
    ELASTIC_PROTOCOL: str = Field(env="ELASTIC_PROTOCOL", default="http")
    SIZE_FOR_LOAD_TO_ELASTICSEARCH: int = Field(
        env="SIZE_FOR_LOAD_TO_ELASTICSEARCH", default=20
    )
    POSTGRES_PASSWORD: str = Field(env="POSTGRES_PASSWORD", default="123qwe")
    POSTGRES_HOST: str = Field(env="POSTGRES_HOST", default="localhost")
    POSTGRES_PORT: int = Field(env="POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = Field(env="POSTGRES_DB", default="movies_database")
    POSTGRES_USER: str = Field(env="POSTGRES_USER", default="app")
    SIZE: int = Field(env="SIZE", default=10)
    MOVIES_INDEX: str = Field(env="MOVIES_INDEX", default="movies")
    GENRES_INDEX: str = Field(env="GENRES_INDEX", default="ganres")
    PERSONS_INDEX: str = Field(env="PERSONS_INDEX", default="persons")
    AUTH_HOST: str = Field(
        env="AUTH_HOST",
        default="http://127.0.0.1:8001/api/v1/users/auth_check/"
    )

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()
