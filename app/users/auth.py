# import datetime
from jose import jwt
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi import HTTPException

from app.config import settings
from app.users.service import UserService
from app.users.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.SECRET_ALGORITHM,
    )
    return encoded_jwt


async def auth_user(username: str, password: str) -> Users | None:
    user = await UserService.find_one_or_none(
        username=username,
    )
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
