import asyncio
import os

import aiohttp
import aioredis
import jwt
import orjson
import pytest

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from tests.functional.settings import BASE_DIR, config
from utils.constants import ACCESS_TOKEN_TTL, USER_ROLES, PERMISSIONS

pytest_plugins = (
    "tests.functional.utils.film_conftest",
    "tests.functional.utils.persons_conftest",
    "tests.functional.utils.genre_conftest",
)


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
    pool = aioredis.ConnectionsPool(
        (config.REDIS_HOST, config.REDIS_PORT),
        minsize=10,
        maxsize=20,
    )
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
async def session(create_token):
    token = create_token
    headers = {
        "Authorization": f"Bearer {token.decode('utf-8')}",
    }
    session = aiohttp.ClientSession(headers=headers)
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


@pytest.fixture(scope='session')
def create_token() -> bytes:
    payload = {}
    now = datetime.now(timezone.utc)
    expire = datetime.timestamp(now + timedelta(hours=ACCESS_TOKEN_TTL))
    payload["type"] = "access"
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = "123-456"
    payload["perms"] = [{USER_ROLES.admin: PERMISSIONS.admin_permissions}]

    yield jwt.encode(payload, config.JWT_SECRET)
