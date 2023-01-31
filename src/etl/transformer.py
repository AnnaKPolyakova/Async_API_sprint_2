import logging
from typing import List

from etl.defines import GENRES, PERSONS

logger = logging.getLogger(__name__)


class GenreDataTransformer:
    def __init__(self, genres_data: List):
        self.genres_data: List = genres_data
        self.genres_list: List = list()

    def genres_to_list_of_dict(self):
        logger.debug("Start transformation objects for updating")
        for obj in self.genres_data:
            del obj["modified"]
            self.genres_list.append(
                {
                    "_index": GENRES,
                    "_id": obj["id"],
                    "_source": obj,
                }
            )
        logger.debug("End transformation genres objects for updating")
        return self.genres_list


class PersonDataTransformer:
    def __init__(self, genres_data: List):
        self.persons_data: List = genres_data
        self.persons_list: List = list()

    def genres_to_list_of_dict(self):
        logger.debug("Start transformation objects for updating")
        for obj in self.persons_data:
            del obj["modified"]
            self.persons_list.append(
                {
                    "_index": PERSONS,
                    "_id": obj["id"],
                    "_source": obj,
                }
            )
        logger.debug("End transformation genres objects for updating")
        return self.persons_list
