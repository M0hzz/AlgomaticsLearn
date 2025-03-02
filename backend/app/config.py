import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "algomatics_db")

    # JWT Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "https://editor.wix.com",           # Wix Editor
        "https://www.wixsite.com",          # Live Wix site
        "https://dev.mywixsite.com",        # Dev environment
        "https://staging.mywixsite.com",    # Staging environment
        "http://localhost:3000",            # Local React development
    ]

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

    # Hugging Face Integration
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()