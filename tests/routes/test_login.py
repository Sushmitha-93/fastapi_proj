import pytest
from httpx import AsyncClient
from fastapi import status
from tests.util import get_test_user


@pytest.mark.asyncio
async def test_correct_login(client: AsyncClient):
    # Get test user
    user = await get_test_user()

    # Test successful login
    response = await client.post("/api/auth/login", data={'username': user['email'], 'password': user['password']})
    assert response.status_code == 200

    # Check if response payload has tokens
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None


@pytest.mark.asyncio
async def test_incorrect_login(client: AsyncClient):
    # Get test user
    user = await get_test_user()

    # Test wrong password
    response = await client.post("/api/auth/login", data={'username': user['email'], 'password': 'wrongpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password'

    # Test wrong username
    response = await client.post("/api/auth/login", data={'username': 'wrongusername', 'password': user['password']})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password'


@pytest.mark.asyncio
async def test_invalid_login_payload(client: AsyncClient):
    # Get test user
    user = await get_test_user()

    # Test missing username
    response = await client.post("/api/auth/login", data={'password': user['password']})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
