import http

import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.persons import PERSONS_DATA

pytestmark = pytest.mark.asyncio


async def test_persons_search(
        session, es_client, persons_index_create, es_write_persons_data
):
    url_template = "{service_url}/api/v1/persons/"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert len(body) == test_settings.SIZE


async def test_get_person(
        session, es_client, persons_index_create, es_write_persons_data
):
    url_template = "{service_url}/api/v1/persons/{id}/"
    id = PERSONS_DATA[0]["id"]
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.OK


async def test_persons_search_with_sort(
        session, es_client, persons_index_create, es_write_persons_data
):
    url_template = "{service_url}/api/v1/persons/?sort=full_name:asc"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body[0]["id"] == 'efdd1787-8871-4aa9-b1d7-f68e55b913ed'


async def test_persons_search_with_filter(
        session, es_client, persons_index_create, es_write_persons_data
):
    url_template = "{service_url}/api/v1/persons/" \
                   "?filter=full_name::Mark Hamill"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body[0]["id"] == '26e83050-29ef-4163-a99d-b546cac208f8'


async def test_persons_search_with_page(
        session, es_client, persons_index_create, es_write_persons_data
):
    url_template = "{service_url}/api/v1/persons/?page=100"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert len(body) == 0


async def test_get_persons_with_id_not_exists(
        session, es_client, persons_index_create,
):
    url_template = "{service_url}/api/v1/persons/{id}/"
    id = 1
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_get_persons_with_id_invalid(
        session, es_client, persons_index_create,
):
    url_template = "{service_url}/api/v1/persons/{id}/"
    id = '4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f'
    url = url_template.format(service_url=test_settings.SERVICE_URL, id=id)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_persons_search_with_page_invalid(
        session, es_client, persons_index_create, es_write_persons_data
):
    url_template = "{service_url}/api/v1/persons/?page=hh"
    url = url_template.format(service_url=test_settings.SERVICE_URL)
    async with session.get(url) as response:
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY
