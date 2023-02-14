import http

import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.movies import MOVIES_DATA

pytestmark = pytest.mark.asyncio


async def test_movies_search(
        session, es_client, movies_index_create, es_write_movies_data
):
    url_template = "{service_url}/api/v1/films/"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert len(body) == test_settings.SIZE


async def test_get_movie(
        session, es_client, movies_index_create, es_write_movies_data
):
    url_template = "{service_url}/api/v1/films/{id}/"
    id = MOVIES_DATA[0]["id"]
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.OK


async def test_movies_search_with_sort(
        session, es_client, movies_index_create, es_write_movies_data
):
    url_template = "{service_url}/api/v1/films/?sort=imdb_rating:asc"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body[0]["id"] == '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f'


async def test_movies_search_with_filter(
        session, es_client, movies_index_create, es_write_movies_data
):
    url_template = "{service_url}/api/v1/films/?filter=imdb_rating::8.7"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body[0]["id"] == '0312ed51-8833-413f-bff5-0e139c11264a'


async def test_movies_search_with_page(
        session, es_client, movies_index_create, es_write_movies_data
):
    url_template = "{service_url}/api/v1/films/?page=100"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert len(body) == 0


async def test_get_movie_with_id_not_exists(
        session, es_client, movies_index_create
):
    url_template = "{service_url}/api/v1/films/{id}/"
    id = 1
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_get_movie_with_id_invalid(
        session, es_client, movies_index_create
):
    url_template = "{service_url}/api/v1/films/{id}/"
    id = '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f'
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_movies_search_with_page_invalid(
        session, es_client, movies_index_create, es_write_movies_data
):
    url_template = "{service_url}/api/v1/films/?page=hh"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY
