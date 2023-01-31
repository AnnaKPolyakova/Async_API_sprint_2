import logging

import psycopg2
from psycopg2.extras import DictCursor

from core.config import settings

logger = logging.getLogger(__name__)


def get_postgres_connect():
    dsl = {
        "dbname": settings["POSTGRES_DB"],
        "user": settings["POSTGRES_USER"],
        "password": settings["POSTGRES_PASSWORD"],
        "host": settings["POSTGRES_HOST"],
        "port": settings["POSTGRES_PORT"],
    }
    logger.debug("Connected to PostgresQL Database")
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)
