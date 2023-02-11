import asyncio
import json

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from src.etl.defines import GENRE_INDEX, MOVIES_INDEX, PERSON_INDEX
from tests.functional.settings import test_settings
from tests.functional.testdata.genres import GENRES_DATA
from tests.functional.testdata.movies import MOVIES_DATA
from tests.functional.testdata.persons import PERSONS_DATA

TEST_GENRES = test_settings.GENRES_INDEX
TEST_PERSONS = test_settings.PERSONS_INDEX
TEST_MOVIES = test_settings.MOVIES_INDEX


def get_str_query(index, data):
    bulk_query = []
    for row in data:
        bulk_query.extend(
            [
                json.dumps({'index': {'_index': index, '_id': row['id']}}),
                json.dumps(row)
            ]
        )
    return '\n'.join(bulk_query) + '\n'


@pytest.fixture(scope='session')
async def es_client():
    url = test_settings.ELASTIC_PROTOCOL + "://" + \
          test_settings.ELASTIC_HOST_TEST + ":" + \
          test_settings.ELASTIC_PORT
    es_client = AsyncElasticsearch(hosts=[url])
    yield es_client
    await es_client.close()


@pytest.fixture
async def movies_index_create(es_client):
    await es_client.indices.create(
        index=TEST_MOVIES, ignore=400, body=MOVIES_INDEX
    )
    yield es_client
    await es_client.indices.delete(index=TEST_MOVIES)


@pytest.fixture
async def genres_index_create(es_client):
    await es_client.indices.create(
        index=TEST_GENRES, ignore=400, body=GENRE_INDEX
    )
    yield es_client
    await es_client.indices.delete(index=TEST_GENRES)


@pytest.fixture
async def persons_index_create(es_client):
    await es_client.indices.create(
        index=TEST_PERSONS, ignore=400, body=PERSON_INDEX
    )
    yield es_client
    await es_client.indices.delete(index=TEST_PERSONS)


@pytest.fixture
async def es_write_movies_data(es_client, movies_index_create):
    str_query = get_str_query(TEST_MOVIES, MOVIES_DATA)
    await es_client.bulk(str_query, refresh=True)
    yield es_client


@pytest.fixture
async def es_write_persons_data(es_client, persons_index_create):
    str_query = get_str_query(TEST_PERSONS, PERSONS_DATA)
    await es_client.bulk(str_query, refresh=True)
    yield es_client


@pytest.fixture
async def es_write_genres_data(es_client, genres_index_create):
    str_query = get_str_query(TEST_GENRES, GENRES_DATA)
    await es_client.bulk(str_query, refresh=True)
    yield es_client


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
