import logging

from src.core.config import settings

logger = logging.getLogger(__name__)


class GenreDataTransformer:

    def __init__(self, genres_data: list):
        self.genres_data: list = genres_data
        self.genres_list: list = list()

    def genres_to_list_of_dict(self):
        logger.debug("Start transformation objects for updating")
        for obj in self.genres_data:
            del obj["modified"]
            self.genres_list.append(
                {
                    "_index": settings.GENRES_INDEX,
                    "_id": obj["id"],
                    "_source": obj,
                }
            )
        logger.debug("End transformation genres objects for updating")
        return self.genres_list


class PersonDataTransformer:
    def __init__(self, genres_data: list):
        self.persons_data: list = genres_data
        self.persons_list: list = list()

    def genres_to_list_of_dict(self):
        logger.debug("Start transformation objects for updating")
        for obj in self.persons_data:
            del obj["modified"]
            self.persons_list.append(
                {
                    "_index": settings.PERSONS_INDEX,
                    "_id": obj["id"],
                    "_source": obj,
                }
            )
        logger.debug("End transformation genres objects for updating")
        return self.persons_list
