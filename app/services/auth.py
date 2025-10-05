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
- ALGORITHM: The algorithm used for signing JWT tokens.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt
from pwdlib import PasswordHash
from fastapi import HTTPException
from services.config import settings

# Password hashing context
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
            return password_hash.hash(password)
        except Exception as e:
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
            return password_hash.verify(plain_password, hashed_password)
        except Exception as e:
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
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
            to_encode.update({"exp": expire})
            encoded_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return encoded_token
        except Exception as e:
            print(e)
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
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token expired") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token") from e
