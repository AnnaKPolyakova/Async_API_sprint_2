import datetime
import logging
from typing import Set

import redis

from core.config import settings
from etl.db.postgres import get_postgres_connect
from etl.defines import (
    LAST_EXTRACT_DATA_FOR_GENRE,
    LAST_EXTRACT_DATA_FOR_PERSON
)

MODELS_AND_FILTERS_FIELDS = {
    LAST_EXTRACT_DATA_FOR_PERSON: "person_film_work__person__modified__gt",
    LAST_EXTRACT_DATA_FOR_GENRE: "genre_film_work__genre__modified__gt",
}

MODELS_AND_DATA_FIELDS = {
    "genre": LAST_EXTRACT_DATA_FOR_GENRE,
    "person": LAST_EXTRACT_DATA_FOR_PERSON,
}

logger = logging.getLogger(__name__)

FINISHED_GETTING_OBJECTS = (
    "Finished getting {objects} for updating. " "Total count: {count}"
)
NEW_DATES_SET = "New date {date} for updating was set for {obj_name}"


class Extractor:
    def __init__(self):
        self.redis_db: redis.Redis = redis.Redis(
            host=settings["REDIS_HOST"],
            port=settings["REDIS_PORT"],
            db=0
        )
        self.pg_connect = get_postgres_connect()
        self.genre_new_date: datetime = None
        self.person_new_date: datetime = None
        self._new_objects_set: Set = set()

    def _get_last_data(self, key_name: str):
        self.redis_db.delete(key_name)
        data = self.redis_db.get(key_name)
        if not data:
            return
        data = data.decode("utf-8")
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f%z")

    def set_last_data(self):
        if self.genre_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_GENRE, str(self.genre_new_date)
            )
            logger.debug(
                NEW_DATES_SET.format(
                    date=self.genre_new_date,
                    obj_name=LAST_EXTRACT_DATA_FOR_GENRE
                )
            )
        if self.person_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_PERSON, str(self.person_new_date)
            )
            logger.debug(
                NEW_DATES_SET.format(
                    date=self.person_new_date,
                    obj_name=LAST_EXTRACT_DATA_FOR_PERSON
                )
            )

    def _get_sql_request(self, sql: str, date: str):
        with self.pg_connect.cursor() as cursor:
            cursor.execute(sql, [date])
            columns = [col[0] for col in cursor.description]
            cursor = cursor.fetchall()
            rows = [dict(zip(columns, row)) for row in cursor]
        return rows

    def _get_updated_genres(self):
        date = self._get_last_data(LAST_EXTRACT_DATA_FOR_GENRE)
        sql = (
            "SELECT content.genre.id, content.genre.name, "
            "content.genre.description, "
            "content.genre.modified "
            "FROM content.genre "
            "{filter}"
            "ORDER BY content.genre.modified ASC "
        )
        if date is None:
            sql = sql.format(filter=" ")
        else:
            sql = sql.format(filter="WHERE content.genre.modified >  %s ")
        objects = self._get_sql_request(sql, date)
        if len(objects) > 0:
            self.genre_new_date = max(obj["modified"] for obj in objects)
        return objects

    def get_updated_persons(self):
        date = self._get_last_data(LAST_EXTRACT_DATA_FOR_GENRE)
        sql = (
            "SELECT id, full_name, gender, modified "
            "FROM content.person "
            "{filter} "
            "ORDER BY modified ASC "
        )
        if date is None:
            sql = sql.format(filter=" ")
        else:
            sql = sql.format(filter="WHERE content.person.modified >  %s ")
        objects = self._get_sql_request(sql, date)
        if len(objects) > 0:
            self.genre_new_date = max(obj["modified"] for obj in objects)
        return objects

    def get_updated_genres_and_persons(self):
        logger.debug("Start getting objects for updating")
        updated_genres = self._get_updated_genres()
        logger.debug(
            FINISHED_GETTING_OBJECTS.format(
                objects="genres", count=len(updated_genres)
            )
        )
        updated_persons = self.get_updated_persons()
        logger.debug(
            FINISHED_GETTING_OBJECTS.format(
                objects="person", count=len(updated_persons)
            )
        )
        return updated_genres, updated_persons
