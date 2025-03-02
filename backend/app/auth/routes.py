from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from bson.objectid import ObjectId
from app.auth.utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user
)
from app.db import get_collection, USERS_COLLECTION
from app.config import settings

router = APIRouter()

# Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    users_collection = get_collection(USERS_COLLECTION)

    # Check if username exists
    if await users_collection.find_one({"username": user_data.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists
    if await users_collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["is_active"] = True
    user_dict["is_admin"] = False

    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)

    return User(**user_dict)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token."""
    users_collection = get_collection(USERS_COLLECTION)

    # Find user by username
    user = await users_collection.find_one({"username": form_data.username})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "id": str(user["_id"])},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user = Depends(get_current_active_user)):
    """Get current user profile."""
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"],
        "is_active": current_user["is_active"]
    }