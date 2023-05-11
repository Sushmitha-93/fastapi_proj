from app.schemas.userSchema import UserSignUp
from app.models.userModel import User
from app.core.security import getHashedPassword, verify_password
from typing import Optional


class UserService:
    @staticmethod
    async def create_user(data: UserSignUp):
        new_user = User(
            email=data.email,
            username=data.username,
            hashedPassword=getHashedPassword(data.password),
            firstName=data.firstName,
            lastName=data.lastName
        )
        await new_user.insert()
        return new_user

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashedPassword):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def get_user_by_id(userid: str) -> Optional[User]:
        user = await User.find_one(User.userid == userid)
        return user
