from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal  #
from backend.services.auth_service import register_user, authenticate_user
from pydantic import BaseModel

router = APIRouter()

# Define request model
class AuthRequest(BaseModel):
    username: str
    password: str
    account_type: str  # New field for account type

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup endpoint
@router.post("/signup")
def signup(request: AuthRequest, db: Session = Depends(get_db)):
    user = register_user(db, request.username, request.password, request.account_type)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid account type or user exists")
    return {"message": "User created successfully"}

# Login endpoint
@router.post("/login")
def login(request: AuthRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "account_type": user.account_type}
