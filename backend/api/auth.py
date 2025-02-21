from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "password":
        return {"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@auth_router.get("/users/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"user": "Authenticated User", "token": token}
