from fastapi import APIRouter, Depends
from app.models.userModel import User
from app.schemas.usermood_schema import CreateMoodSchema, MoodSchemaOut
from app.api.auth.user_deps import get_current_user
from app.services.usermood_service import UserMoodService

user_mood_router = APIRouter()


@user_mood_router.post('/add', summary="Creates a new user mood", response_model=MoodSchemaOut)
async def create_user_mood(data: CreateMoodSchema, current_user: User = Depends(get_current_user)):
    return await UserMoodService.create_user_mood(user=current_user, data=data)


@user_mood_router.get('/moodFrequency', summary="Returns the frequency of each mood for the current user")
async def get_user_mood_frequency(current_user: User = Depends(get_current_user)):
    return await UserMoodService.get_user_mood_frequency(user=current_user)
