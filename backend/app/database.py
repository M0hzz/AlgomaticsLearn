from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLite connection (for user data)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./math_algo.db")

# Create engine - note the extra arguments needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# MongoDB connection (for algorithm data)
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
mongo_client = MongoClient(MONGO_URL)
algorithm_db = mongo_client.algorithm_database

# Database dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()