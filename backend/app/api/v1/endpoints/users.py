from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.schemas.user import UserCreate, User
from backend.app.models.user import User as UserModel
from backend.app.core.security import get_password_hash
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
