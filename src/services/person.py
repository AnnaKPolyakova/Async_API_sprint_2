from functools import lru_cache
from typing import List, Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.utils import get_list_objects_cache_key


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def get_persons_list(
            self, size, page, sort, genre
    ) -> Optional[List[Person]]:
        persons = await self._persons_from_cache(size, page, sort, genre)
        if not persons:
            persons = await self._get_persons_from_elastic(
                size, page, sort, genre
            )
            await self._put_persons_to_cache(persons, size, page, sort, genre)
        persons = await self._get_persons_from_elastic(size, page, sort, genre)
        return persons

    async def _get_person_from_elastic(
            self, person_id: str
    ) -> Optional[Person]:
        try:
            doc = await self.elastic.get("persons", person_id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])

    async def _get_persons_from_elastic(
        self, size, page, sort, filter
    ) -> Optional[List[Person]]:
        data = {
            "index": "persons",
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
        return [Person(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(person.id, person.json())
        await self.redis.expire(
            person.id, settings["FILM_CACHE_EXPIRE_IN_SECONDS"]
        )

    async def _persons_from_cache(
        self, size, page, sort, genre
    ) -> Optional[List[Person]]:
        key = await get_list_objects_cache_key(
            "person", size, page, sort, genre
        )
        data = await self.redis.get(key)
        if not data:
            return []
        return [Person.parse_raw(item) for item in orjson.loads(data)]

    async def _put_persons_to_cache(self, persons, size, page, sort, genre):
        if persons is None:
            persons = []
        key = await get_list_objects_cache_key(
            "person", size, page, sort, genre
        )
        await self.redis.set(
            key,
            orjson.dumps([person.json(by_alias=True) for person in persons]),
        )
        await self.redis.expire(key, settings["FILM_CACHE_EXPIRE_IN_SECONDS"])


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
