import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_not_authorized(client: AsyncClient):
    """Test user not authorized if required"""
    resp = await client.get("/api/closestHappyPlace/37.3366834/37.3366834")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    headers = {"AUTHORIZATION": "Bearer eyJhbGciOiJIUzI1NiIsInR5ExM"}
    resp = await client.get("/api/closestHappyPlace/37.3366834/37.3366834", headers=headers)
    assert resp.status_code == status.HTTP_403_FORBIDDEN
