"""
Configuration file for environment variables and global settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Keep Notes API"
    VERSION: str = "1.0.0"

    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:root123@localhost:3306/keepnotes"
    )

    # JWT settings
    # SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
