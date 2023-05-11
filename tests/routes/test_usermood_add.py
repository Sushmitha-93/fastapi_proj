import pytest
from httpx import AsyncClient
from fastapi import status
from tests.util import get_test_user, get_auth_headers

data = {
    "mood": "happy",
    "location": [37.3366834, -121.8894127]
}


@pytest.mark.asyncio
async def test_usermood_add(client: AsyncClient):
    # Get test user
    user = await get_test_user()
    headers = await get_auth_headers(client=client, email=user['email'], password=user['password'])

    # Add usermood correct data and headers
    response = await client.post("/api/usermood/add", json=data, headers=headers)
    assert response.status_code == 200

    # Check response payload structure
    payload = response.json()
    assert "userid" in payload
    assert "mood" in payload
    assert "location" in payload
    assert "date" in payload


@pytest.mark.asyncio
async def test_usermood_add_authorization(client: AsyncClient):

    # Test with no authorization header
    response = await client.post("/api/usermood/add", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'

    # Test with invalid authorization header
    headers = {"AUTHORIZATION": "Bearer eyJhbGciOiJIUzI1NiIsInR5ExM"}
    response = await client.post("/api/usermood/add", json=data, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'Could not validate credentials'


@pytest.mark.asyncio
async def test_usermood_add_invalid_payload(client: AsyncClient):
    # Get test user
    user = await get_test_user()
    headers = await get_auth_headers(client=client, email=user['email'], password=user['password'])

    # Add usermood incorrect data and headers
    response = await client.post("/api/usermood/add", json={}, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'field required'
    assert response.json()['detail'][0]['type'] == 'value_error.missing'

    # Add usermood incorrect data and headers
    response = await client.post("/api/usermood/add", json={"mood": "happy"}, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'field required'
    assert response.json()['detail'][0]['type'] == 'value_error.missing'

    # Add usermood incorrect data and headers
    response = await client.post("/api/usermood/add", json={"location": [37.3366834, -121.8894127]}, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'field required'
    assert response.json()['detail'][0]['type'] == 'value_error.missing'

    # Add usermood incorrect data and headers
    response = await client.post("/api/usermood/add", json={"mood": "happy", "location": [37.3366834, -121.8894127], "extra": "extra"}, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'extra fields not permitted'
    assert response.json()['detail'][0]['type'] == 'value_error.extra'
