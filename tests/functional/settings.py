import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from tests.functional.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env_test"), override=True)


class TestSettings(BaseSettings):
    ELASTIC_HOST_TEST: str
    ELASTIC_HOST: str
    ELASTIC_PORT: str
    ELASTIC_PROTOCOL: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PROTOCOL: str
    SERVICE_URL: str
    MOVIES_INDEX: str
    GENRES_INDEX: str
    SIZE: int
    PERSONS_INDEX: str = Field(env='PERSONS_INDEX')

    class Config:
        env_file = os.path.join(BASE_DIR, ".env_test")
        env_file_encoding = "utf-8"


logging_config.dictConfig(LOGGING)

test_settings = TestSettings()
