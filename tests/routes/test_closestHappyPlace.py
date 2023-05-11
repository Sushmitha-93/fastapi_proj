import pytest
from httpx import AsyncClient
from fastapi import status
from tests.util import get_test_user, get_auth_headers, create_usermoods_test_data


@pytest.mark.asyncio
async def test_closestHappyPlace(client: AsyncClient):
    # insert test data
    await create_usermoods_test_data(client=client)
    # Get test user
    user = await get_test_user()
    headers = await get_auth_headers(client=client, email=user['email'], password=user['password'])

    # Add usermood correct data and headers
    response = await client.get("/api/closestHappyPlace/37.3366834/-120.8894127", headers=headers)
    assert response.status_code == 200

    # Check response payload structure
    payload = response.json()
    assert "nearestLocation" in payload
    assert "distance" in payload
    assert "name" in payload
    assert "address" in payload


@pytest.mark.asyncio
async def test_closestHappyPlace_authorization(client: AsyncClient):
    # Test with no authorization header
    response = await client.get("/api/closestHappyPlace/37.3366834/-121.8894127")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'

    # Test with invalid authorization header
    headers = {"AUTHORIZATION": "Bearer eyJhbGciOiJIUzI1NiIsInR5ExM"}
    response = await client.get("/api/closestHappyPlace/37.3366834/-121.8894127", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'Could not validate credentials'
