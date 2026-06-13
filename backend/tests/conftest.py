import os

os.environ["ENV_FILE"] = ".env.test"

import pytest
import pytest_asyncio
from app.core.database import Base, engine
from app.core.redis import close_redis, get_redis, initialize_redis
import app.models
from app.main import app
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture


@pytest_asyncio.fixture(autouse=True)
async def reset_database():
    await engine.dispose()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def reset_redis():
    try:
        await initialize_redis()
        redis = await get_redis()
        await redis.flushdb()
    except Exception as exc:
        pytest.skip(f"Redis test database is not available: {exc}")

    yield

    redis = await get_redis()
    await redis.flushdb()
    await close_redis()


@fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def authenticated_client(client):
    user = {
        "email": "test@example.com",
        "password": "password123",
    }

    await client.post(
        "/auth/register",
        json=user,
    )

    response = await client.post(
        "/auth/login",
        json=user,
    )

    token = response.json()["access_token"]

    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )

    return client
