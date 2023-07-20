import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import Redis


# Possible improvements:
# * create separated database for tests
# * add supporting multiple databases for multi threading for pytest
@pytest.fixture
async def redis() -> Redis:
    from app.api.dependencies.redis import get_redis

    return await get_redis()


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def client(app, redis):
    await redis.flushall()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
