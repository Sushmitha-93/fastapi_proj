"""
Common test utilities
"""

from httpx import AsyncClient
from app.models.userModel import User
from app.core.security import getHashedPassword
import json


async def get_test_user():
    """Adds test users to user collection"""
    if (await User.find_one(User.email == "user@test.com") is None):
        test_user = User(
            email="user@test.com",
            username="user12",
            hashedPassword=getHashedPassword("test1234"),
            firstName="test",
            lastName="test"
        )
        await test_user.insert()
    return {"email": "user@test.com", "password": "test1234"}


async def get_auth_headers(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    """Returns the authorization headers for a user"""
    data = {'username': email, 'password': password}
    response = await client.post("/api/auth/login", data=data)
    return {"AUTHORIZATION": "Bearer " + response.json()['access_token']}


async def create_usermoods_test_data(client: AsyncClient):
    user = await get_test_user()
    headers = await get_auth_headers(client=client, email=user['email'], password=user['password'])
    # Test data
    data = [{"mood": "neutral", "location": [37.33554078709717, -121.88504833738618]},
            {"mood": "happy", "location": [
                37.33554078709717, -121.88504833738618]},
            {"mood": "sad", "location": [
                37.33554078709717, -121.88504833738618]},
            {"mood": "happy", "location": [
                37.33472615937162, -121.88876585481954]},
            {"mood": "happy", "location": [37.3366834, -121.8894127]},
            {"mood": "sad", "location": [37.3366834, -121.8894127]}
            ]

    for i in data:
        response = await client.post("/api/usermood/add", json=i, headers=headers)
