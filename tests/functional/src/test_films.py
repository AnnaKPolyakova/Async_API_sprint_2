import pytest
from tests.functional.settings import test_settings
from tests.functional.testdata.movies import MOVIES_DATA


@pytest.mark.asyncio
async def test_movies_search(
        session, es_client, movies_index_create, es_write_movies_data
):
    print(test_settings.SERVICE_URL)
    url = test_settings.SERVICE_URL + '/api/v1/films/'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert len(body) == test_settings.SIZE


@pytest.mark.asyncio
async def test_get_movie(
        session, es_client, movies_index_create, es_write_movies_data
):
    id = MOVIES_DATA[0]["id"]
    url = test_settings.SERVICE_URL + '/api/v1/films/' + id + '/'
    async with session.get(url) as response:
        assert response.status == 200


@pytest.mark.asyncio
async def test_movies_search_with_sort(
        session, es_client, movies_index_create, es_write_movies_data
):
    url = test_settings.SERVICE_URL + '/api/v1/films/?sort=imdb_rating:asc'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert body[0]["id"] == '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f'


@pytest.mark.asyncio
async def test_movies_search_with_filter(
        session, es_client, movies_index_create, es_write_movies_data
):
    url = test_settings.SERVICE_URL + '/api/v1/films/?filter=imdb_rating::8.7'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert body[0]["id"] == '0312ed51-8833-413f-bff5-0e139c11264a'


@pytest.mark.asyncio
async def test_movies_search_with_page(
        session, es_client, movies_index_create, es_write_movies_data
):
    url = test_settings.SERVICE_URL + '/api/v1/films/?page=100'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert len(body) == 0
