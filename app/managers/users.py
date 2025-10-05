"""
UserService Module

This module handles user management-related operations, including adding, retrieving, updating, 
and deleting users from the database. It interacts with the database layer, schema definitions, 
and authentication services.

Dependencies:
- AuthService: For password hashing and related authentication utilities.
- conn: Database connection for interacting with the KnowledgeBase.
- UserEntity, UsersEntity: Schema definitions for user data validation and transformation.
- logging: For logging various actions and errors related to user operations.
"""

import logging
from models.user import UserEntityTransformer
from fastapi import HTTPException
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import User

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

class FetchService:
    """Service class for user-related database operations such as adding users."""

    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        """
        Fetches a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            dict: The user details transformed into a proper format.

        Raises:
            HTTPException: If the user is not found or if there is a failure during the database operation.
        """
        logger.info("Attempting to fetch user with email: %s", email)

        try:
            # user = db.query(models.User).filter(models.User.user_email == email).first()
            user = db.query(User).filter(User.user_email == email).first()
            if not user:
                logger.warning("User with email %s not found.", email)
                raise HTTPException(status_code=400, detail="User not found")
            logger.info("User %s fetched successfully.", email)
            return UserEntityTransformer.user_entity(user)

        except HTTPException as e:
            # Re-raise the HTTPException for cases like 400 errors.
            raise e
        except Exception as e:
            logger.error("Failed to fetch user %s: %s", email, str(e))
            raise HTTPException(status_code=500, detail="Failed to fetch user") from e
