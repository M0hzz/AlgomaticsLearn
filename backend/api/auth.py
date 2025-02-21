from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from services.auth_service import hash_password, verify_password, create_access_token
from models.user import User

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User signup route
@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password and create user
    new_user = User(username=username, password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# User login route
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # Find user in DB
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
