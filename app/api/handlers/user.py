from fastapi import status, HTTPException, APIRouter
from app.schemas.userSchema import UserSignUp, UserOut
from app.services.userService import UserService
import pymongo.errors

user_router = APIRouter()


@user_router.post('/signup', summary="Creates a new user", response_model=UserOut)
async def create_user(data: UserSignUp):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError as e:  # To catch duplicate email or username
        raise HTTPException(
            # print(e)
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this " +
            list(e.details['keyValue'].keys())[0]+" already exists"
        )
