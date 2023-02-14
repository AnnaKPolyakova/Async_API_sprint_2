from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio.client import Redis

from src.core.config import settings
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.cacher import Cacher
from src.services.objects_finder import ObjectsFinder
from src.services.searcher import Searcher


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    cacher = Cacher(redis, settings.MOVIES_INDEX)
    searcher = Searcher(elastic, settings.MOVIES_INDEX)
    return ObjectsFinder(cacher, searcher)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    cacher = Cacher(redis, settings.GENRES_INDEX)
    searcher = Searcher(elastic, settings.GENRES_INDEX)
    return ObjectsFinder(cacher, searcher)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    cacher = Cacher(redis, settings.PERSONS_INDEX)
    searcher = Searcher(elastic, settings.PERSONS_INDEX)
    return ObjectsFinder(cacher, searcher)
