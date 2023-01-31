import logging
from typing import Dict

from elasticsearch import Elasticsearch, helpers

from core.config import settings
from etl.defines import GENRE_INDEX, GENRES, PERSON_INDEX, PERSONS

logger = logging.getLogger(__name__)

LOADER_ERROR = "Loading invalid, error: {error}"


class Loader:
    def __init__(self):
        self.elastic: Elasticsearch = self._get_elastic()

    @staticmethod
    def _get_elastic():
        ELASTIC_PROTOCOL = settings["ELASTIC_PROTOCOL"]
        ELASTIC_HOST = settings["ELASTIC_HOST"]
        ELASTIC_PORT = settings["ELASTIC_PORT"]
        url = ELASTIC_PROTOCOL + "://" + ELASTIC_HOST + ":" + str(ELASTIC_PORT)
        return Elasticsearch(url)

    def _person_index_create(self):
        self.elastic.indices.create(
            index=PERSONS, ignore=400, body=PERSON_INDEX
        )

    def _genre_index_create(self):
        self.elastic.indices.create(index=GENRES, ignore=400, body=GENRE_INDEX)

    def _load_data(self, data: Dict):
        helpers.bulk(self.elastic, data)

    def load_persons_data(self, data: Dict):
        if len(data) == 0:
            return
        try:
            self._person_index_create()
            self._load_data(data)
        except Exception as error:
            msg = "Persons loading get error {error}"
            logger.debug(msg.format(error=error))
            self._load_data(data)
        logger.debug("Persons loading done")
        return

    def load_genres_data(self, data: Dict):
        if len(data) == 0:
            return
        try:
            self._genre_index_create()
            self._load_data(data)
        except Exception as error:
            msg = "Genres loading get error {error}"
            logger.debug(msg.format(error=error))
            self._load_data(data)
        logger.debug("Genres loading done")
        return
