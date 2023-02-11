import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.persons import PERSONS_DATA


@pytest.mark.asyncio
async def test_persons_search(
        session, es_client, persons_index_create, es_write_persons_data
):
    url = test_settings.SERVICE_URL + '/api/v1/persons/'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert len(body) == test_settings.SIZE


@pytest.mark.asyncio
async def test_get_person(
        session, es_client, persons_index_create, es_write_persons_data
):
    id = PERSONS_DATA[0]["id"]
    url = test_settings.SERVICE_URL + '/api/v1/persons/' + id + '/'
    async with session.get(url) as response:
        assert response.status == 200


@pytest.mark.asyncio
async def test_persons_search_with_sort(
        session, es_client, persons_index_create, es_write_persons_data
):
    url = test_settings.SERVICE_URL + '/api/v1/persons/?sort=full_name:asc'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert body[0]["id"] == 'efdd1787-8871-4aa9-b1d7-f68e55b913ed'


@pytest.mark.asyncio
async def test_persons_search_with_filter(
        session, es_client, persons_index_create, es_write_persons_data
):
    url = test_settings.SERVICE_URL + \
          '/api/v1/persons/?filter=full_name::Mark Hamill'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert body[0]["id"] == '26e83050-29ef-4163-a99d-b546cac208f8'


@pytest.mark.asyncio
async def test_persons_search_with_page(
        session, es_client, persons_index_create, es_write_persons_data
):
    url = test_settings.SERVICE_URL + '/api/v1/persons/?page=100'
    async with session.get(url) as response:
        body = await response.json()
        assert response.status == 200
        assert len(body) == 0
