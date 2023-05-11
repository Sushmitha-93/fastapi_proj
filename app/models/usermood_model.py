from beanie import Document, Link
from pydantic import Field
from datetime import datetime
from typing import Tuple
from app.models.userModel import User


class UserMood(Document):
    user: Link[User]
    mood: str
    location: Tuple[float, float]
    date: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user_moods"
