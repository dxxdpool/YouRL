from app.main import app
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture


@fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
