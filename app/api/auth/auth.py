from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.services.userService import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.userSchema import UserOut
from app.models.userModel import User
from app.api.auth.user_deps import get_current_user

auth_router = APIRouter()


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user.userid),
        "refresh_token": create_refresh_token(user.userid),
    }
