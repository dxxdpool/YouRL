from app.core.config import settings
from redis.asyncio import Redis

redis_client: Redis | None = None


async def initialize_redis():
    global redis_client

    redis_client = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )

    await redis_client.ping()


async def close_redis():
    global redis_client

    if redis_client is not None:
        await redis_client.aclose()


async def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis has not been initialized.")

    return redis_client
