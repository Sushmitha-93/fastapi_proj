import pytest
from httpx import AsyncClient
from fastapi import status
from tests.util import get_test_user, get_auth_headers, create_usermoods_test_data


@pytest.mark.asyncio
async def test_mood_frequency(client: AsyncClient):
    # insert test data
    await create_usermoods_test_data(client=client)
    # Get test user
    user = await get_test_user()
    headers = await get_auth_headers(client=client, email=user['email'], password=user['password'])

    # Test successful mood frequency
    response = await client.get("/api/usermood/moodFrequency", headers=headers)
    assert response.status_code == 200
    payload = response.json()[0]
    assert "mood" in payload
    assert "count" in payload


async def test_mood_frequency_authorization(client: AsyncClient):
    # Test with no authorization header
    response = await client.get("/api/usermood/moodFrequency")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'

    # Test with invalid authorization header
    headers = {"AUTHORIZATION": "Bearer eyJhbGciOiJIUzI1NiIsInR5ExM"}
    response = await client.get("/api/usermood/moodFrequency", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'Could not validate credentials'
