# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection (for user data)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/math_algo_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# MongoDB connection (for algorithm data)
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
mongo_client = MongoClient(MONGO_URL)
algorithm_db = mongo_client["algorithm_database"] #using db name directly instead of referring to it

# Redis connection (for caching)
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# Database dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()