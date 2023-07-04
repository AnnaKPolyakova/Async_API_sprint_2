import logging
from time import sleep

from psycopg2 import OperationalError

from src.core.config import settings
from src.etl.backoff import backoff
from src.etl.extractor import Extractor
from src.etl.loader import Loader
from src.etl.transformer import GenreDataTransformer, PersonDataTransformer

logger = logging.getLogger(__name__)

LOADED_DATA = "Loaded data for {number} part"
DATA_LOADING_WAS_COMPLETED = (
    "Data loading was completed for all {number} parts"
)

SIZE_FOR_LOAD_TO_ELASTICSEARCH = settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH


class DBUpdater:
    def __init__(self):
        self.loader = Loader()
        self.extractor = Extractor()
        self.genres_data: list[dict] = list()
        self.persons_data: list[dict] = list()
        self.genres_data_list: list[dict] = list()
        self.persons_data_list: list[dict] = list()
        self.persons_data_transformer = PersonDataTransformer
        self.genres_data_transformer = GenreDataTransformer

    def _load_data(self, data: list[dict]):
        self.loader.load_persons_data(data)
        self.loader.load_genres_data(data)

    def _load_genres(self):
        len_genres_data = len(self.genres_data)
        if len_genres_data == 0:
            logger.debug("Nothing to update for genres")
        else:
            self.genres_data_list = self.genres_data_transformer(
                self.genres_data
            ).genres_to_list_of_dict()
            count = len_genres_data // SIZE_FOR_LOAD_TO_ELASTICSEARCH
            if count > 0 and len_genres_data % SIZE_FOR_LOAD_TO_ELASTICSEARCH:
                count += 1
            for i in range(count):
                data_to_load = self.genres_data_list[
                    SIZE_FOR_LOAD_TO_ELASTICSEARCH
                    * i: SIZE_FOR_LOAD_TO_ELASTICSEARCH
                    * (i + 1)
                ]
                self.loader.load_genres_data(data_to_load)
                logger.debug(LOADED_DATA.format(number=i + 1))
            logger.debug(DATA_LOADING_WAS_COMPLETED.format(numbers=count))

    def _load_persons(self):
        len_persons_data = len(self.persons_data)
        if len_persons_data == 0:
            logger.debug("Nothing to update for persons")
        else:
            self.persons_data_list = self.persons_data_transformer(
                self.persons_data
            ).genres_to_list_of_dict()
            count = len_persons_data // SIZE_FOR_LOAD_TO_ELASTICSEARCH
            if count > 0 and len_persons_data % SIZE_FOR_LOAD_TO_ELASTICSEARCH:
                count += 1
            for i in range(count):
                data_to_load = self.persons_data_list[
                    SIZE_FOR_LOAD_TO_ELASTICSEARCH
                    * i: SIZE_FOR_LOAD_TO_ELASTICSEARCH
                    * (i + 1)
                ]
                self.loader.load_persons_data(data_to_load)
                logger.debug(LOADED_DATA.format(number=i + 1))
            logger.debug(DATA_LOADING_WAS_COMPLETED.format(numbers=count))

    @backoff((OperationalError,))
    @backoff((ConnectionError,))
    def update_data_in_elasticsearch(self):
        logger.debug("Start update data in elasticsearch")
        (
            self.genres_data,
            self.persons_data,
        ) = self.extractor.get_updated_genres_and_persons()
        self._load_genres()
        self._load_persons()
        self.extractor.set_last_data()


if __name__ == "__main__":
    while True:
        DBUpdater().update_data_in_elasticsearch()
        sleep(5)
