import asyncio
import aiohttp
import aioredis
import pytest
import os
import orjson

from dataclasses import dataclass

from aioredis import Redis
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch
from tests.functional.settings import BASE_DIR, config

from tests.functional.utils.elastic_test_schemas import (
    filmworks_index_schema, 
    persons_index_schema, 
    genres_index_schema
)
from tests.functional.utils.elastic_test_service import ElasticTestService


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


@pytest.fixture()
async def clear_redis_cache():
    pool = aioredis.ConnectionsPool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    redis = Redis(pool)
    await redis.flushall()
    yield
    redis.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}')
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
        url = f'http://{config.SERVICE_HOST}:{config.SERVICE_PORT}' + method
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
        with open(os.path.join(BASE_DIR, 'testdata', filename)) as file:
            return orjson.loads(file.read())
    return load_data


@pytest.fixture
async def prepare_film_service(es_client, load_test_films_to_es):
    """Create test index for tests and delete index after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(config.ELASTIC_INDEX['movies'], filmworks_index_schema)
    await es_service.bulk_store(config.ELASTIC_INDEX['movies'], load_test_films_to_es)
    yield
    await es_service.delete_index(config.ELASTIC_INDEX['movies'])


@pytest.fixture
async def prepare_person_service(es_client, load_test_persons_to_es):
    """Create test person_ index to es and delete after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(config.ELASTIC_INDEX['persons'], persons_index_schema)
    await es_service.bulk_store(config.ELASTIC_INDEX['persons'], load_test_persons_to_es)
    yield
    await es_service.delete_index(config.ELASTIC_INDEX['persons'])


@pytest.fixture
def load_test_films_to_es(load_test_data):
    return load_test_data('films_loads_to_es.json')


@pytest.fixture
def api_films_v1_url():
    return '/api/v1/film/'


@pytest.fixture
def api_film_by_id_v1_url():
    return '/api/v1/film/{film_id}'


@pytest.fixture
async def prepare_genre_service(es_client, load_test_genres_to_es):
    """Create test person_ index to es and delete after."""
    es_service = ElasticTestService(es_client)
    await es_service.create_index(config.ELASTIC_INDEX['genres'], genres_index_schema)
    await es_service.bulk_store(config.ELASTIC_INDEX['genres'], load_test_genres_to_es)
    yield
    await es_service.delete_index(config.ELASTIC_INDEX['genres'])


@pytest.fixture
def api_genre_v1_url():
    return '/api/v1/genre/'


@pytest.fixture
def api_genre_by_id_v1_url():
    return '/api/v1/genre/{genre_id}'


def api_persons_v1_url():
    return '/api/v1/person/'


@pytest.fixture
def api_person_by_id_v1_url():
    return '/api/v1/person/{person_id}'


@pytest.fixture
def api_search_film_by_person():
    return '/api/v1/person/{person_id}/film/'


