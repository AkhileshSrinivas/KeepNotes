"""
UserService Module

This module handles user management-related operations, including adding, retrieving, updating, 
and deleting users from the database. It interacts with the database layer, schema definitions, 
and authentication services.

Dependencies:
- AuthService: For password hashing and related authentication utilities.
- conn: Database connection for interacting with the KnowledgeBase.
- UserEntity, UsersEntity: Schema definitions for user data validation and transformation.
"""

from models.user import UserEntityTransformer
from fastapi import HTTPException
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import User

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

        try:
            user = db.query(User).filter(User.user_email == email).first()
            if not user:
                raise HTTPException(status_code=400, detail="User not found")
            return UserEntityTransformer.user_entity(user)

        except HTTPException as e:
            # Re-raise the HTTPException for cases like 400 errors.
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to fetch user") from e
