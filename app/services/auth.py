"""
Module: Authentication Utilities

This module provides authentication-related utilities, including password hashing,
password verification, and JWT token generation/validation.

It leverages bcrypt for secure password hashing and JWT for access token management.
The AuthService class contains static methods for these operations.

Features:
- Hash plaintext passwords using bcrypt.
- Verify plaintext passwords against hashed counterparts.
- Create JWT tokens with expiration.
- Decode and validate JWT tokens, handling expiration and invalid token scenarios.

Dependencies:
- jwt: For encoding and decoding JSON Web Tokens (JWT).
- passlib: For secure password hashing and verification.
- fastapi: For HTTP exceptions used in error handling.

Configuration:
- SECRET_KEY: The secret key used for signing JWT tokens.
- ALGORITHM: The algorithm used for signing JWT tokens (e.g., HS256).
"""

import logging
from datetime import datetime, timedelta, timezone
from jose import jwt
# from passlib.context import CryptContext
from pwdlib import PasswordHash
from fastapi import HTTPException
from services.config import settings

# Set up a logger for the module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Secret key for JWT token signing
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash.recommended()


class AuthService:
    """Service class for authentication-related utilities."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the given password using bcrypt.

        Args:
            password (str): The plaintext password.

        Returns:
            str: The hashed password.

        Raises:
            HTTPException: If there is an error while hashing the password.
        """
        try:
            logger.info("Hashing password")
            # return pwd_context.hash(password)
            return password_hash.hash(password)
        except Exception as e:
            logger.error("Failed to hash password: %s",e)
            raise HTTPException(status_code=500, detail="Failed to hash password") from e

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plaintext password against its hashed counterpart.

        Args:
            plain_password (str): The plaintext password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the password matches, otherwise False.

        Raises:
            HTTPException: If there is an error while verifying the password.
        """
        try:
            logger.info("Verifying password")
            # return pwd_context.verify(plain_password, hashed_password)
            return password_hash.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error("Failed to verify password: %s", e)
            raise HTTPException(status_code=500, detail="Failed to verify password") from e

    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Creates a JWT token with the specified payload and expiration.

        Args:
            data (dict): The payload data to encode in the token.
            expires_delta (timedelta, optional): Token expiration time. Defaults to 15 minutes.

        Returns:
            str: Encoded JWT token.

        Raises:
            HTTPException: If there is an error while creating the access token.
        """
        try:
            logger.info("Creating access token")
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
            to_encode.update({"exp": expire})
            encoded_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            logger.info("Access token created successfully")
            return encoded_token
        except Exception as e:
            logger.error("Failed to create access token: %s", e)
            raise HTTPException(status_code=500, detail="Failed to create access token") from e

    @staticmethod
    async def decode_access_token(token: str) -> dict:
        """
        Decodes and validates a JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token payload.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            logger.info("Decoding access token")
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            logger.info("Token decoded successfully")
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            logger.error("Token expired: %s", e)
            raise HTTPException(status_code=401, detail="Token expired") from e
        except jwt.InvalidTokenError as e:
            logger.error("Invalid token: %s", e)
            raise HTTPException(status_code=401, detail="Invalid token") from e
