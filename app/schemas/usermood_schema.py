from pydantic import BaseModel, Extra
from datetime import datetime
from uuid import UUID
from beanie import Link


class CreateMoodSchema(BaseModel):
    mood: str
    location: tuple[float, float]

    class Config:
        extra = Extra.forbid


class MoodSchemaOut(BaseModel):
    userid: UUID
    mood: str
    location: tuple[float, float]
    date: datetime


class ClosestHappyPlaceOutSchema(BaseModel):
    location: tuple[float, float]
    # To do: add distance to the response
    address: str
    name: str
