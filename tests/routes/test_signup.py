import pytest
from httpx import AsyncClient
from fastapi import status

user = {
    "email": "test@test.com",
    "username": "test",
    "password": "test123",
    "firstName": "John",
    "lastName": "Doe"
}


@pytest.mark.asyncio
async def test_signup(client: AsyncClient):
    """Test successful signup"""
    response = await client.post("/api/user/signup", json=user)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_signup_validation(client: AsyncClient):
    """Test email input validation"""
    data = {**user, "email": "test@test"}
    response = await client.post("/api/user/signup", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()[
        "detail"][0]["msg"] == 'value is not a valid email address'

    """Test password input validation"""
    data = {**user, "password": "test"}
    response = await client.post("/api/user/signup", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()[
        "detail"][0]["msg"] == 'ensure this value has at least 5 characters'


@pytest.mark.asyncio
async def test_signup_duplicate(client: AsyncClient):
    """Test duplicate email and username"""
    response = await client.post("/api/user/signup", json=user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[
        "detail"] == 'User with this username already exists'

    """Test duplicate email"""
    data = {**user, "username": "test12"}
    response = await client.post("/api/user/signup", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == 'User with this email already exists'
