import asyncio
import aiohttp
import pytest
import os
import orjson

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch
from src.core import config
from src.tests.functional.settings import SERVICE_URL, ELASTIC_URL


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=ELASTIC_URL)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def load_test_data():
    def load_data(filename: str):
        with open(os.path.join(config.BASE_DIR, 'tests', 'functional', 'testdata', filename)) as file:
            return orjson.loads(file.read())
    return load_data


@pytest.fixture
def api_films_v1_url():
    return '/api/v1/film/'


@pytest.fixture
def api_film_by_id_v1_url():
    return '/api/v1/film/{film_id}'
