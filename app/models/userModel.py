from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional


class User(Document):
    userid: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashedPassword: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    disabled: Optional[bool] = False

    class Settings:
        name = "users"  # Maps to the collection name in MongoDB
