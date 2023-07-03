import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from tests.functional.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env_test"), override=True)


class TestSettings(BaseSettings):
    ELASTIC_HOST_TEST: str = Field(env="ELASTIC_HOST_TEST", default="127.0.0.1")
    ELASTIC_HOST: str = Field(env="ELASTIC_HOST", default="movies-elastic")
    ELASTIC_PORT: str = Field(env="ELASTIC_PORT", default="9200")
    ELASTIC_PROTOCOL: str = Field(env="ELASTIC_PROTOCOL", default="http")
    REDIS_HOST: str = Field(env="REDIS_HOST", default="redis")
    REDIS_PORT: str = Field(env="REDIS_PORT", default="6376")
    REDIS_PROTOCOL: str = Field(env="REDIS_PROTOCOL", default="redis")
    SERVICE_URL: str = Field(env="SERVICE_URL", default="http://0.0.0.0:8000")
    MOVIES_INDEX: str = Field(env="MOVIES_INDEX", default="movies_test")
    GENRES_INDEX: str = Field(env="GENRES_INDEX", default="genres_test")
    SIZE: int = Field(env="SIZE", default=2)
    PERSONS_INDEX: str = Field(env='PERSONS_INDEX', default="persons_test")

    class Config:
        env_file = os.path.join(BASE_DIR, ".env_test")
        env_file_encoding = "utf-8"


logging_config.dictConfig(LOGGING)

test_settings = TestSettings()
