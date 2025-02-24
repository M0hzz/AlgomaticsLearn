#SQL models and table

from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

from backend.app.users.schemas import UserInDBBase

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=3, max_length=50)
    password: constr(min_length=8)

class UserUpdate(UserBase):
    password: Optional[constr(min_length=8)] = None

class UserInDB(UserBase):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str