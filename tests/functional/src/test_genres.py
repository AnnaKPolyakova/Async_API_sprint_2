import http

import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.genres import GENRES_DATA

pytestmark = pytest.mark.asyncio


async def test_genres_search(
        session, es_client, genres_index_create, es_write_genres_data
):
    url_template = "{service_url}/api/v1/genres/"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert len(body) == test_settings.SIZE


async def test_get_genre(
        session, es_client, genres_index_create, es_write_genres_data
):
    url_template = "{service_url}/api/v1/genres/{id}/"
    id = GENRES_DATA[0]["id"]
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.OK


async def test_genres_search_with_filter(
        session, es_client, genres_index_create, es_write_genres_data
):
    url_template = "{service_url}/api/v1/genres/?filter=name::Adventure"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body[0]["id"] == '120a21cf-9097-479e-904a-13dd7198c1dd'


async def test_genres_search_with_page(
        session, es_client, genres_index_create, es_write_genres_data
):
    url_template = "{service_url}/api/v1/genres/?page=100"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert len(body) == 0


async def test_genres_search_with_sort(
        session, es_client, genres_index_create, es_write_genres_data
):
    url_template = "{service_url}/api/v1/genres/?sort=name:desc"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body[0]["id"] == '526769d7-df18-4661-9aa6-49ed24e9dfd8'


async def test_get_genre_with_id_not_exists(
        session, es_client, genres_index_create,
):
    url_template = "{service_url}/api/v1/genres/{id}/"
    id = 1
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_get_genre_with_id_invalid(
        session, es_client, genres_index_create,
):
    url_template = "{service_url}/api/v1/genres/{id}/"
    id = '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f'
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_genre_search_with_page_invalid(
        session, es_client, genres_index_create, es_write_genres_data
):
    url_template = "{service_url}/api/v1/genres/?page=hh"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY
