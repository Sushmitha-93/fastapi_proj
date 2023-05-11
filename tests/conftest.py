import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.core.config import settings
from app.main import app

# Override config settings before loading the app
settings.TESTING = True


@pytest.fixture()
async def client():
    """Async server client that handles lifespan and teardown"""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            try:
                yield ac
            except Exception as exc:  # pylint: disable=broad-except
                print(exc)
