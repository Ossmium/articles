from jose import jwt, JWTError
from datetime import datetime
from fastapi import Request, HTTPException, status, Depends

from app.config import settings
from app.users.service import UserService


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка авторизации",
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.SECRET_ALGORITHM,
        )
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    expire = payload.get("exp")
    if not expire or int(expire) < int(datetime.utcnow().timestamp()):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка авторизации",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка авторизации",
        )

    user = await UserService.find_by_id(id=int(user_id))
    if not user:
        raise HTTPException(
            status.HTTP_404_UNAUTHORIZED,
            detail="Данного пользователя нет",
        )

    if user.is_banned:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Пользователь заблокирован",
        )
    return user
