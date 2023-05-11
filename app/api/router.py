from fastapi import APIRouter
from app.api.handlers.user import user_router
from app.api.auth.auth import auth_router
from app.api.handlers.user_mood import user_mood_router
from app.api.handlers.closest_happy_place import closest_happy_place

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=["users"])
router.include_router(auth_router, prefix='/auth', tags=["auth"])
router.include_router(user_mood_router, prefix='/usermood', tags=["usermood"])
router.include_router(
    closest_happy_place, prefix='/closestHappyPlace', tags=["closestHappyPlace"])
