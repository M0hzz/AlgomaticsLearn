from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, List
from sqlalchemy.orm import Session
from datetime import timedelta

from . import schemas
from backend.app.core.config import settings
from backend.app.core.security import create_access_token
from ..dependencies import get_db, get_current_active_user, get_current_admin_user
from . import service

router = APIRouter()

@router.post("/auth/register", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserCreate,
) -> Any:
    """Create new user"""
    user = service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )
    user = service.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists"
        )
    user = service.create_user(db, obj_in=user_in)
    return user

@router.post("/auth/login", response_model=schemas.Token)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login"""
    user = service.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/users/me", response_model=schemas.User)
def read_user_me(
        current_user: schemas.User = Depends(get_current_active_user),
) -> Any:
    """Get current user"""
    return current_user

@router.put("/users/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserUpdate,
        current_user: schemas.User = Depends(get_current_active_user),
) -> Any:
    """Update current user"""
    user = service.update_user(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/users", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Depends(get_current_admin_user),
) -> Any:
    """Retrieve users"""
    users = service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        current_user: schemas.User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
) -> Any:
    """Get a specific user by id"""
    user = service.get_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if not current_user.is_admin and user.id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Not enough permissions"
        )
    return user