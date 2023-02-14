import logging

from elasticsearch import Elasticsearch, helpers

from src.core.config import settings
from src.etl.defines import GENRE_INDEX, PERSON_INDEX

logger = logging.getLogger(__name__)

LOADER_ERROR = "Loading invalid, error: {error}"


class Loader:
    def __init__(self):
        self.elastic: Elasticsearch = self._get_elastic()

    @staticmethod
    def _get_elastic():
        ELASTIC_PROTOCOL = settings.ELASTIC_PROTOCOL
        ELASTIC_HOST = settings.ELASTIC_HOST
        ELASTIC_PORT = settings.ELASTIC_PORT
        url_template = "{elastic_protocol}://{elastic_host}:{elastic_port}"
        url = url_template.format(
            elastic_protocol=ELASTIC_PROTOCOL,
            elastic_host=ELASTIC_HOST,
            elastic_port=str(ELASTIC_PORT)
        )
        return Elasticsearch(url)

    def _person_index_create(self):
        self.elastic.indices.create(
            index=settings.PERSONS_INDEX, ignore=400, body=PERSON_INDEX
        )

    def _genre_index_create(self):
        self.elastic.indices.create(
            index=settings.GENRES_INDEX, ignore=400, body=GENRE_INDEX
        )

    def _load_data(self, data: dict):
        helpers.bulk(self.elastic, data)

    def load_persons_data(self, data: dict):
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

    def load_genres_data(self, data: dict):
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
