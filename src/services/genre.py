from functools import lru_cache
from typing import List, Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.utils import get_list_objects_cache_key


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def get_genres_list(
            self, size, page, sort, genre
    ) -> Optional[Genre]:
        genres = await self._genres_from_cache(size, page, sort, genre)
        if not genres:
            genres = await self._get_genres_from_elastic(
                size, page, sort, genre
            )
            await self._put_genres_to_cache(genres, size, page, sort, genre)
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get("genres", genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _get_genres_from_elastic(
            self, size, page, sort, filter
    ) -> List[Genre]:
        data = {
            "index": "genres",
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
        return [Genre(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(genre.id, genre.json())
        await self.redis.expire(
            genre.id, settings["FILM_CACHE_EXPIRE_IN_SECONDS"]
        )

    async def _genres_from_cache(self, size, page, sort, genre) -> List[Genre]:
        key = await get_list_objects_cache_key(
            "genre", size, page, sort, genre
        )
        data = await self.redis.get(key)
        if not data:
            return []
        return [Genre.parse_raw(item) for item in orjson.loads(data)]

    async def _put_genres_to_cache(self, genres, size, page, sort, genre):
        if genres is None:
            genres = []
        key = await get_list_objects_cache_key(
            "genre", size, page, sort, genre
        )
        await self.redis.set(
            key,
            orjson.dumps([genre.json(by_alias=True) for genre in genres]),
        )
        await self.redis.expire(key, settings["FILM_CACHE_EXPIRE_IN_SECONDS"])


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
