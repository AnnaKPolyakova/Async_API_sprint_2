import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.genres import GENRES_DATA


@pytest.mark.asyncio
async def test_genres_search(
        session, es_client, genres_index_create, es_write_genres_data
):
    url = test_settings.SERVICE_URL + '/api/v1/genres/'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert len(body) == test_settings.SIZE


@pytest.mark.asyncio
async def test_get_genre(
        session, es_client, genres_index_create, es_write_genres_data
):
    id = GENRES_DATA[0]["id"]
    url = test_settings.SERVICE_URL + '/api/v1/genres/' + id + '/'
    async with session.get(url) as response:
        assert response.status == 200


@pytest.mark.asyncio
async def test_genres_search_with_filter(
        session, es_client, genres_index_create, es_write_genres_data
):
    url = test_settings.SERVICE_URL + '/api/v1/genres/?filter=name::Adventure'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert body[0]["id"] == '120a21cf-9097-479e-904a-13dd7198c1dd'


@pytest.mark.asyncio
async def test_genres_search_with_page(
        session, es_client, genres_index_create, es_write_genres_data
):
    url = test_settings.SERVICE_URL + '/api/v1/genres/?page=100'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert len(body) == 0


@pytest.mark.asyncio
async def test_genres_search_with_sort(
        session, es_client, genres_index_create, es_write_genres_data
):
    url = test_settings.SERVICE_URL + '/api/v1/genres/?sort=name:desc'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert body[0]["id"] == '526769d7-df18-4661-9aa6-49ed24e9dfd8'
