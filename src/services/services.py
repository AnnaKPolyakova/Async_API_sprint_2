from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from etl.defines import MOVIES, GENRES, PERSONS
from services.casher import Casher
from services.objects_finder import ObjectsFinder
from services.searcher import Searcher


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    casher = Casher(redis, MOVIES)
    searcher = Searcher(elastic, MOVIES)
    return ObjectsFinder(casher, searcher)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    casher = Casher(redis, GENRES)
    searcher = Searcher(elastic, GENRES)
    return ObjectsFinder(casher, searcher)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ObjectsFinder:
    casher = Casher(redis, PERSONS)
    searcher = Searcher(elastic, PERSONS)
    return ObjectsFinder(casher, searcher)
