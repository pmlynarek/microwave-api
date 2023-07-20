import redis.asyncio as redis

from app.core.config import settings


async def get_redis() -> redis.Redis:
    r = await redis.from_url(settings.REDIS_URL)

    await r.ping()
    return r
