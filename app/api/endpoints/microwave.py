from fastapi import APIRouter
from fastapi import Depends
from redis.asyncio import Redis

from app.api.constants import REDIS_MICROWAVE_CURRENT_STATE_KEY
from app.api.dependencies.auth import validate_token
from app.api.dependencies.microwave import get_microwave_state
from app.api.dependencies.redis import get_redis
from app.api.schemas.microwave import MicrowaveState
from app.api.utils.redis import save_object_to_redis
from app.core.logging import get_logger

logger = get_logger(__name__)


router: APIRouter = APIRouter(prefix="/microwave", tags=["microwave"])


# Implemented this way, because it was faster
# It shouldn't be a problem to use websockets as well: https://fastapi.tiangolo.com/advanced/websockets/
@router.get(
    "",
    response_model=MicrowaveState,
    summary="Get current state of office microwave",
)
async def retrieve_microwave_state(
    microwave_state: MicrowaveState = Depends(get_microwave_state),
):
    return microwave_state


@router.post(
    "/power/add",
    response_model=MicrowaveState,
    summary="Increase office microwave power by 10%",
)
async def increase_microwave_power(
    redis: Redis = Depends(get_redis),
    microwave_state: MicrowaveState = Depends(get_microwave_state),
):
    microwave_state = microwave_state.inscrease_power()
    await save_object_to_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY, microwave_state)

    return microwave_state


@router.post(
    "/power/sub",
    response_model=MicrowaveState,
    summary="Decrease office microwave power by 10%",
)
async def decrease_microwave_power(
    redis: Redis = Depends(get_redis),
    microwave_state: MicrowaveState = Depends(get_microwave_state),
):
    microwave_state = microwave_state.decrease_power()
    await save_object_to_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY, microwave_state)

    return microwave_state


@router.post(
    "/timer/add",
    response_model=MicrowaveState,
    summary="Increase office microwave timer by 10s",
)
async def increase_microwave_timer(
    redis: Redis = Depends(get_redis),
    microwave_state: MicrowaveState = Depends(get_microwave_state),
):
    microwave_state = microwave_state.increase_timer()
    await save_object_to_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY, microwave_state)

    return microwave_state


@router.post(
    "/timer/sub",
    response_model=MicrowaveState,
    summary="Decrease office microwave timer by 10s",
)
async def decrease_microwave_timer(
    redis: Redis = Depends(get_redis),
    microwave_state: MicrowaveState = Depends(get_microwave_state),
):
    microwave_state = microwave_state.decrease_timer()
    await save_object_to_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY, microwave_state)

    return microwave_state


@router.post(
    "/cancel",
    response_model=MicrowaveState,
    dependencies=[Depends(validate_token)],
    summary="Cancel heating in office microwave",
)
async def cancel_microwave(
    redis: Redis = Depends(get_redis),
    microwave_state: MicrowaveState = Depends(get_microwave_state),
):
    microwave_state = microwave_state.cancel()
    await save_object_to_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY, microwave_state)

    return microwave_state
