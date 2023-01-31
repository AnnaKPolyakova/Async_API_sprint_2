from typing import List, Union, Optional
from aioredis import Redis
import orjson
from elasticsearch import NotFoundError

from core.config import settings
from models.film import Film
from models.person import Person
from models.genre import Genre

from services.abc_services.abs_casher import ABSCasher

from services.defines import INDEXES_AND_MODELS


class Casher(ABSCasher):
    INDEXES_AND_MODELS = INDEXES_AND_MODELS

    def __init__(self, redis: Redis, index: str):
        self.redis = redis
        self.index = index
        self.model = INDEXES_AND_MODELS[self.index]

    async def put_by_id_to_cache(self, obj) -> None:
        key = f"{self.index}:{obj.id}"
        await self.redis.set(key, obj.json())
        await self.redis.expire(key, settings["FILM_CACHE_EXPIRE_IN_SECONDS"])

    async def put_objs_to_cache(
            self,
            objs: Union[List[Film], List[Person], List[Genre]],
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None],
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
        await self.redis.expire(key, settings["FILM_CACHE_EXPIRE_IN_SECONDS"])

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
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> List:
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
