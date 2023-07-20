from datetime import datetime
from datetime import timedelta
from typing import Optional

import pytest
from fastapi import status
from httpx import AsyncClient
from redis.asyncio import Redis

from app.api.constants import REDIS_MICROWAVE_CURRENT_STATE_KEY
from app.api.schemas.microwave import MicrowaveState
from app.api.utils.redis import save_object_to_redis


async def setup_microwave_state(
    redis: Redis, power: Optional[int] = 500, timer_end_at: Optional[datetime] = None
) -> MicrowaveState:
    new_timer_end_at = timer_end_at or datetime.now() + timedelta(days=1)
    microwave_state = MicrowaveState(power=power, timer_end_at=new_timer_end_at)
    await save_object_to_redis(redis, REDIS_MICROWAVE_CURRENT_STATE_KEY, microwave_state)

    return microwave_state


@pytest.mark.anyio
async def test_retrieve_microwave_state(client: AsyncClient, redis: Redis):
    # Get microwave state without any data in Redis
    response = await client.get("/api/microwave")
    assert response.status_code == 200

    response_data: dict = response.json()
    assert response_data["power"] == 600

    # Get microwave state with data in Redis
    microwave_state = await setup_microwave_state(redis)

    response = await client.get("/api/microwave")

    assert response.status_code == status.HTTP_200_OK

    response_data: dict = response.json()
    assert response_data["power"] == microwave_state.power
    assert datetime.fromisoformat(response_data["timer_end_at"]) == microwave_state.timer_end_at


@pytest.mark.anyio
async def test_increase_microwave_power_no_redis_data(client: AsyncClient, redis: Redis):
    response = await client.post("/api/microwave/power/add")
    assert response.status_code == status.HTTP_200_OK

    response_data: dict = response.json()
    assert response_data["power"] == 660


@pytest.mark.anyio
@pytest.mark.parametrize("power,expected_status", [(500, status.HTTP_200_OK), (1199, status.HTTP_400_BAD_REQUEST)])
async def test_increase_microwave_power(power: int, expected_status: int, client: AsyncClient, redis: Redis):
    microwave_state = await setup_microwave_state(redis, power=power)

    response = await client.post("/api/microwave/power/add")
    assert response.status_code == expected_status

    if expected_status != 200:
        return

    response_data: dict = response.json()
    assert response_data["power"] == 550
    assert datetime.fromisoformat(response_data["timer_end_at"]) == microwave_state.timer_end_at


@pytest.mark.anyio
async def test_decrease_microwave_power_no_redis_data(client: AsyncClient, redis: Redis):
    response = await client.post("/api/microwave/power/sub")
    assert response.status_code == status.HTTP_200_OK

    response_data: dict = response.json()
    assert response_data["power"] == 540


@pytest.mark.anyio
@pytest.mark.parametrize("power,expected_status", [(500, status.HTTP_200_OK), (301, status.HTTP_400_BAD_REQUEST)])
async def test_decrease_microwave_power(power: int, expected_status: int, client: AsyncClient, redis: Redis):
    microwave_state = await setup_microwave_state(redis, power=power)

    response = await client.post("/api/microwave/power/sub")
    assert response.status_code == expected_status

    if expected_status != 200:
        return

    response_data: dict = response.json()
    assert response_data["power"] == 450
    assert datetime.fromisoformat(response_data["timer_end_at"]) == microwave_state.timer_end_at


@pytest.mark.anyio
async def test_increase_microwave_timer_no_redis_data(client: AsyncClient, redis: Redis):
    response = await client.post("/api/microwave/timer/add")
    assert response.status_code == status.HTTP_200_OK

    response_data: dict = response.json()
    assert response_data["power"] == 600


@pytest.mark.anyio
async def test_increase_microwave_timer(client: AsyncClient, redis: Redis):
    microwave_state = await setup_microwave_state(redis)

    response = await client.post("/api/microwave/timer/add")
    assert response.status_code == status.HTTP_200_OK

    response_data: dict = response.json()
    assert response_data["power"] == microwave_state.power
    assert datetime.fromisoformat(response_data["timer_end_at"]) == (
        microwave_state.timer_end_at + timedelta(seconds=10)
    )


@pytest.mark.anyio
async def test_decrease_microwave_timer_no_redis_data(client: AsyncClient, redis: Redis):
    response = await client.post("/api/microwave/timer/sub")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
@pytest.mark.parametrize(
    "_timedelta,expected_status",
    [
        (timedelta(days=1), status.HTTP_200_OK),
        (timedelta(seconds=5), status.HTTP_200_OK),
    ],
)
async def test_decrease_microwave_timer(_timedelta: timedelta, expected_status: int, client: AsyncClient, redis: Redis):
    timer_end_at = datetime.now() + _timedelta
    microwave_state = await setup_microwave_state(redis, timer_end_at=timer_end_at)

    response = await client.post("/api/microwave/timer/sub")
    assert response.status_code == expected_status

    response_data: dict = response.json()
    assert response_data["power"] == microwave_state.power

    if _timedelta.total_seconds() < 10:
        assert datetime.fromisoformat(response_data["timer_end_at"]).replace(microsecond=0) == (
            microwave_state.timer_end_at - _timedelta
        ).replace(microsecond=0)
    else:
        assert datetime.fromisoformat(response_data["timer_end_at"]) == (
            microwave_state.timer_end_at - timedelta(seconds=10)
        )
