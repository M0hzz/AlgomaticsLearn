from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to the API!"}

@router.get("/health")
def health_check():
    return {"status": "OK"}

@router.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "description": "This is an item"}
