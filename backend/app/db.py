from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB."""
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    db.db = db.client[settings.DATABASE_NAME]
    logger.info("Connected to MongoDB!")

async def close_mongo_connection():
    """Close MongoDB connection."""
    logger.info("Closing MongoDB connection...")
    if db.client:
        db.client.close()
    logger.info("MongoDB connection closed!")

# Collections
def get_collection(collection_name: str):
    """Get MongoDB collection."""
    return db.db[collection_name]

# Collection names
USERS_COLLECTION = "users"
ALGORITHMS_COLLECTION = "algorithms"
DATA_STRUCTURES_COLLECTION = "data_structures"
MATH_TOPICS_COLLECTION = "math_topics"
USER_PROGRESS_COLLECTION = "user_progress"