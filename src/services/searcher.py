from typing import List, Optional, Union

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel

from src.services.abc_services.abs_searcher import ABSSearcher
from src.services.defines import INDEXES_AND_MODELS


class Searcher(ABSSearcher):
    INDEXES_AND_MODELS = INDEXES_AND_MODELS

    def __init__(
            self,
            elastic: AsyncElasticsearch,
            index: str
    ):
        self.elastic = elastic
        self.index = index
        self.model = INDEXES_AND_MODELS[self.index]

    async def get_obj_from_elastic(self, film_id: str) -> Optional[BaseModel]:
        try:
            doc = await self.elastic.get(self.index, film_id)
        except NotFoundError:
            return None
        return self.model(**doc["_source"])

    async def get_objs_from_elastic(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> List[BaseModel]:
        page -= 1
        data = {
            "index": self.index,
            "body": {
                "query": {"match_all": {}},
                "from": page,
            },
            "size": size,
        }
        if sort:
            sort = sort.split(":")
            data["body"]["sort"] = [{sort[0]: sort[1]}]
        if filter:
            filter = filter.split("::")
            if len(filter) == 2:
                data["body"] = {
                    "query": {
                        "bool": {"must": [{"match": {filter[0]: filter[1]}}]}
                    }
                }
        try:
            docs = await self.elastic.search(**data)
        except NotFoundError:
            return []
        return [self.model(**doc["_source"]) for doc in docs["hits"]["hits"]]
