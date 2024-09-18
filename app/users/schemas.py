from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    hashed_password: str
    is_admin: bool


class UserAuthSchema(BaseModel):
    username: str
    password: str


class ChangeIsAdminStatusSchema(BaseModel):
    is_admin: bool


class BanUserSchema(BaseModel):
    is_banned: bool
