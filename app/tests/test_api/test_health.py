import pytest


@pytest.mark.anyio
async def test_healthcheck(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
