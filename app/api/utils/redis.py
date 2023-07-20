import pickle
from typing import Optional

import redis.asyncio as redis

"""
Possible improvements: make "pickling" async.
"""


async def save_object_to_redis(redis_client: redis.Redis, key: str, obj: object):
    await redis_client.set(key, pickle.dumps(obj))


async def get_object_from_redis(redis_client: redis.Redis, key: str) -> Optional[object]:
    raw_data: Optional[bytes] = await redis_client.get(key)
    return pickle.loads(raw_data) if raw_data else None
