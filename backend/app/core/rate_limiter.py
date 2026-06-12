from app.core.config import settings
from app.core.redis import get_redis
from app.models import User
from app.modules.auth.dependencies import get_current_user
from fastapi import Depends, HTTPException, status
from redis.asyncio import Redis

RATE_LIMIT_SCRIPT = """
local current = redis.call("INCR", KEYS[1])

if current == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

local ttl = redis.call("TTL", KEYS[1])

return {current, ttl}
"""


async def rate_limit_create_url(
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
):
    key = f"rate_limit:create_url:{current_user.id}"

    count, ttl = await redis.eval(
        RATE_LIMIT_SCRIPT,
        1,
        key,
        settings.URL_CREATION_RATE_WINDOW_SECONDS,
    )

    if int(count) > settings.URL_CREATION_RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            headers={
                "Retry-After": str(ttl),
            },
        )
