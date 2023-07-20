from datetime import datetime
from typing import Optional

from fastapi import Depends
from redis.asyncio import Redis

from app.api.constants import REDIS_MICROWAVE_CURRENT_STATE_KEY
from app.api.dependencies.redis import get_redis
from app.api.schemas.microwave import MicrowaveState
from app.api.utils.redis import get_object_from_redis


async def get_microwave_state(
    redis: Redis = Depends(get_redis),
):
    microwave_state: Optional[MicrowaveState] = await get_object_from_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY)
    return microwave_state or MicrowaveState(active_till=datetime.now())
