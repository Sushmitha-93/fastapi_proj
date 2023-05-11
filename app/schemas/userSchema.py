from pydantic import Field, EmailStr, BaseModel
from uuid import UUID
from typing import Optional


class UserSignUp(BaseModel):
    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., min_length=4, max_length=30,
                          description="User username")
    password: str = Field(..., min_length=5, max_length=25,
                          description="User password")
    firstName: str = Field(..., min_length=2, max_length=30,
                           description="User first name")
    lastName: str = Field(..., min_length=2, max_length=30,
                          description="User last name")


class UserOut(BaseModel):
    userid: UUID
    email: EmailStr
    username: str
    firstName: Optional[str]
    lastName: Optional[str]
    disabled: Optional[bool]
