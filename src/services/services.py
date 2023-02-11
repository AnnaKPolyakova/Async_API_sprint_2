from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.core.config import settings
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.casher import Casher
from src.services.objects_finder import ObjectsFinder
from src.services.searcher import Searcher


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    casher = Casher(redis, settings.MOVIES_INDEX)
    searcher = Searcher(elastic, settings.MOVIES_INDEX)
    return ObjectsFinder(casher, searcher)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    casher = Casher(redis, settings.GENRES_INDEX)
    searcher = Searcher(elastic, settings.GENRES_INDEX)
    return ObjectsFinder(casher, searcher)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    casher = Casher(redis, settings.PERSONS_INDEX)
    searcher = Searcher(elastic, settings.PERSONS_INDEX)
    return ObjectsFinder(casher, searcher)
