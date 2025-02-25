from fastapi import APIRouter, HTTPException
from backend.app.database import mongo_client, engine
from sqlalchemy import text

router = APIRouter()

@router.get("/mongodb-check")
async def check_mongodb_connection():
    """Check if MongoDB connection is working"""
    try:
        # Check the connection by listing databases
        database_names = mongo_client.list_database_names()

        # Try to insert a test document
        test_db = mongo_client.test_database
        test_collection = test_db.test_collection

        test_id = test_collection.insert_one({"test": "MongoDB connection test"}).inserted_id
        test_collection.delete_one({"_id": test_id})

        return {
            "status": "success",
            "message": "MongoDB connection successful",
            "databases": database_names
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {str(e)}")

@router.get("/sqlite-check")
async def check_sqlite_connection():
    """Check if SQLite connection is working"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                assert row[0] == 1

        return {
            "status": "success",
            "message": "SQLite connection successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQLite connection failed: {str(e)}")

@router.get("/ping")
async def ping():
    """Simple ping endpoint to check if the API is running"""
    return {"ping": "pong", "status": "running"}