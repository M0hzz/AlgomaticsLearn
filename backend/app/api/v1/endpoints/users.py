from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.dependencies import get_current_user
from backend.app.schemas.user import UserCreate, User, Token
from backend.app.models.user import User as UserModel
from backend.app.core.security import get_password_hash, verify_password, create_access_token
from backend.app.database import get_db

router = APIRouter()

@router.post('/users', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_password = get_password_hash(user.password)
    new_user = UserModel(
        email=user.email,
        username = user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", respondse_model=Token)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect username or password')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'Bearer'}

@router.get('/users', response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
