from typing import Optional, Union

import orjson
from elasticsearch import NotFoundError
from redis.asyncio.client import Redis

from src.core.config import settings
from src.models.film import Film
from src.models.genre import Genre
from src.models.person import Person
from src.services.abc_services.abs_cacher import ABSCacher
from src.services.defines import INDEXES_AND_MODELS


class Cacher(ABSCacher):
    INDEXES_AND_MODELS = INDEXES_AND_MODELS

    def __init__(self, redis: Redis, index: str):
        self.redis = redis
        self.index = index
        self.model = INDEXES_AND_MODELS[self.index]

    async def put_by_id_to_cache(self, obj) -> None:
        key = f"{self.index}:{obj.id}"
        await self.redis.set(key, obj.json())
        await self.redis.expire(key, settings.FILM_CACHE_EXPIRE_IN_SECONDS)

    async def put_objs_to_cache(
            self,
            objs: Union[list[Film], list[Person], list[Genre]],
            size: int,
            page: int,
            sort: Optional[str],
            filter: Optional[str],
    ):
        if objs is None:
            objs = []
        key = await self.get_list_objects_cache_key(
            self.index, size, page, sort, filter
        )
        await self.redis.set(
            key,
            orjson.dumps([obj.json(by_alias=True) for obj in objs]),
        )
        await self.redis.expire(key, settings.FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_by_id_from_cache(self, obj_id: str):
        key = f"{self.index}:{obj_id}"
        try:
            data = await self.redis.get(key)
        except NotFoundError:
            return []
        if data is None:
            return []
        data = self.model.parse_raw(data)
        return data

    async def get_objs_from_cache(
            self,
            size: int,
            page: int,
            sort: Optional[str],
            filter: Optional[str]
    ) -> list:
        key = await self.get_list_objects_cache_key(
            self.index, size, page, sort, filter
        )
        data = await self.redis.get(key)
        if not data:
            return []
        return [self.model.parse_raw(item) for item in orjson.loads(data)]

    async def get_list_objects_cache_key(*args) -> str:
        values = [str(value) for value in args]
        values.sort()
        return ":".join(values)
