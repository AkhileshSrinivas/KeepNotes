"""
This module provides user authentication and authorization functionality.

It includes:
- Verifying user credentials.
- Decoding and validating access tokens.
- Checking user roles for access control.
- Retrieving the current active user from the access token.

Dependencies:
- `verify_password`: Validates the password against the stored hash.
- `decode_access_token`: Decodes and verifies the JWT token.
- `get_user`: Fetches user details from the database.
- Pydantic models: For type validation of user and token data.
"""
from typing import Annotated
import logging
from pydantic import ValidationError
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from managers.users import FetchService
from services.auth import AuthService
from schemas.token import TokenData
from schemas.register import UserCreate
from sqlalchemy.orm import Session

from db import database

class AuthUsers:
    """
    Manages user authentication and authorization operations.
    """

    # Class-level variables
    logger = logging.getLogger(__name__)
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Homepage/login_page")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(database.get_db)
    ) -> dict:
        """
        Decode and validate the current user's JWT token.

        Args:
            token (str): JWT access token from the request.

        Returns:
            dict: The current user's details.

        Raises:
            HTTPException: If the token is invalid or the user is not found.
        """
        try:
            payload = await AuthService.decode_access_token(token)
            useremail: str = payload.get("sub")
            if useremail is None:
                raise AuthUsers.credentials_exception
            token_data = TokenData(username=useremail)

            user = await FetchService.get_user_by_email(token_data.username, db)
            if not user:
                raise AuthUsers.credentials_exception
            return user
        except ValidationError as exc:
            AuthUsers.logger.warning("Invalid token provided.")
            raise AuthUsers.credentials_exception from exc
        except Exception as e:
            AuthUsers.logger.error("Error fetching current user: %s", e, exc_info=True)
            raise HTTPException(
                status_code=500, detail="Failed to get the current user!"
            ) from e

    @staticmethod
    async def verify_user(
        current_user: Annotated[UserCreate, Security(get_current_user)]
    ) -> dict:
        """
        Fetch the current active user.

        Args:
            current_user (dict): Current user's details.

        Returns:
            dict: The current active user's details.
        """

        return current_user


