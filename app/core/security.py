from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Optional, Union
from app.core.config import settings
from jose import jwt

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This function is used to hash the password
def getHashedPassword(password: str) -> str:
    return passwordContext.hash(password)


# This function is used to verify the password
def verify_password(password: str, hashedPassword: str) -> bool:
    return passwordContext.verify(password, hashedPassword)


# This function is used to create the JWT access token
def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow(
        ) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# This function is used to create the JWT refresh token
def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow(
        ) + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
