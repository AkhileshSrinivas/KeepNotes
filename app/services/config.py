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
        "DATABASE_URL",
    )

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("TIME_LIMIT")

settings = Settings()
