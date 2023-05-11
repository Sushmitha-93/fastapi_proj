from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.router import router
from app.models.userModel import User
from app.models.usermood_model import UserMood
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    openapi_url=f"{settings.API_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():

    if (settings.TESTING):
        db_client = AsyncIOMotorClient(
            settings.MONGO_CONNECTION_STRING).testdb  # This will be the name of the database
    else:
        db_client = AsyncIOMotorClient(
            settings.MONGO_CONNECTION_STRING).moodSensingDB

    await init_beanie(
        database=db_client,
        document_models=[
            User,
            UserMood
        ],
    )

app.include_router(router, prefix=settings.API_STR)


@app.get("/")
async def root():
    return "Welcome to Python Backend! Go to /docs for API documentation."
