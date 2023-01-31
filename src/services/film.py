from functools import lru_cache
from typing import List, Optional, Union

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.utils import get_list_objects_cache_key


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def get_films_list(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> Optional[Film]:
        films = await self._films_from_cache(size, page, sort, filter)
        if not films:
            films = await self._get_films_from_elastic(
                size, page, sort, filter
            )
            await self._put_films_to_cache(films, size, page, sort, filter)
        films = await self._get_films_from_elastic(size, page, sort, filter)
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get("movies", film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _get_films_from_elastic(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> List[Film]:
        data = {
            "index": "movies",
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
        return [Film(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json())
        await self.redis.expire(
            film.id, settings["FILM_CACHE_EXPIRE_IN_SECONDS"]
        )

    async def _films_from_cache(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None],
    ) -> List[Film]:
        key = await get_list_objects_cache_key(
            "film", size, page, sort, filter
        )
        data = await self.redis.get(key)
        if not data:
            return []
        return [Film.parse_raw(item) for item in orjson.loads(data)]

    async def _put_films_to_cache(
            self,
            films: List[Film],
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None],
    ):
        if films is None:
            films = []
        key = await get_list_objects_cache_key(
            "film", size, page, sort, filter
        )
        await self.redis.set(
            key,
            orjson.dumps([film.json(by_alias=True) for film in films]),
        )
        await self.redis.expire(key, settings["FILM_CACHE_EXPIRE_IN_SECONDS"])


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
