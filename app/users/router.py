from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.models import Users
from app.users.service import UserService
from app.users.schemas import (
    UserRegisterSchema,
    UserAuthSchema,
    ChangeIsAdminStatusSchema,
    BanUserSchema,
)
from app.users.auth import get_password_hash, auth_user, create_access_token
from app.users.dependencies import get_current_user


auth_router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
)

users_router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@auth_router.post("/register")
async def register_user(user_data: UserRegisterSchema):
    existing_user = await UserService.find_one_or_none(
        username=user_data.username,
    )

    if existing_user:
        raise HTTPException(status_code=400)

    hashed_password = get_password_hash(user_data.hashed_password)

    await UserService.add(
        username=user_data.username,
        hashed_password=hashed_password,
        is_admin=user_data.is_admin,
    )


@auth_router.post("/login")
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await auth_user(
        username=user_data.username,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return access_token


@users_router.patch("/{user_id}/is_admin")
async def change_admin_status(
    user_id: int,
    user_status: ChangeIsAdminStatusSchema,
    user: Users = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Нет прав на изменение",
        )

    requested_user: Users = await UserService.find_by_id(id=user_id)
    if not requested_user:
        raise HTTPException(
            status.HTTP_404_FORBIDDEN,
            detail="Нет данного пользователя",
        )

    if requested_user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя назначить забаненного пользователя администратором",
        )

    await UserService.update(
        id=requested_user.id,
        is_admin=user_status.is_admin,
    )
    return user_status.is_admin


@users_router.patch("/{user_id}/ban")
async def ban_user(
    user_id: int,
    user_status: BanUserSchema,
    user: Users = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Нет прав",
        )

    requested_user: Users = await UserService.find_by_id(id=user_id)
    if not requested_user:
        raise HTTPException(
            status.HTTP_404_FORBIDDEN,
            detail="Нет данного пользователя",
        )

    if requested_user.id == user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Нельзя заблокировать самого себя",
        )

    await UserService.update(
        id=requested_user.id,
        is_banned=user_status.is_banned,
    )
    return user_status.is_banned
