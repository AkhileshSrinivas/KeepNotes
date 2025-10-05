"""
Module: User Entity Transformation

This module provides utility functions for transforming MongoDB 
user entities into Python dictionaries. It includes error handling 
for document field mismatches and supports both single and bulk transformations.

Dependencies:
- FastAPI: For raising HTTP exceptions in case of errors.
- Logging: For logging error messages.
"""

import logging
from fastapi import HTTPException

# Set up a logger for the module
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class UserEntityTransformer:
    """
    Handles the transformation of MongoDB user entities into Python dictionaries.
    Provides methods for individual and bulk entity conversions with error handling.
    """

    @staticmethod
    def user_entity(item: dict) -> dict:
        """
        Convert a MongoDB user document into a dictionary.

        Args:
            item (dict): A MongoDB user document.

        Returns:
            dict: A dictionary containing user details such as id, name, email, password, 
                  role, and added date.

        Raises:
            HTTPException: If there is a mismatch in the MongoDB document structure 
                           (e.g., missing fields).
        """
        try:
            # Log the item for debugging purposes
            logger.debug("Transforming user entity: %s", item)

            return {
                "id": str(item.user_id),
                "name": item.user_name,
                "email": item.user_email,
                "password": item.password,
                "last_update": item.last_update,
                "created_on": item.created_on.strftime("%d-%m-%Y")
            }

        except KeyError as e:
            # Log the error and raise an HTTP exception for missing fields
            logger.error("KeyError: %s. Missing key in MongoDB user document.", str(e))
            raise HTTPException(
                status_code=500,
                detail="Key or field mismatch in MongoDB document!"
            ) from e
        except Exception as e:
            # Log any unexpected errors
            logger.error("Unexpected error: %s", str(e))
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred during user entity transformation!"
            ) from e

    @staticmethod
    def users_entity(entity: list) -> list:
        """
        Convert a list of MongoDB user documents into a list of dictionaries.

        Args:
            entity (list): A list of MongoDB user documents.

        Returns:
            list: A list of dictionaries, each containing user details.

        Raises:
            HTTPException: If there is an error during the transformation of any document.
        """
        try:
            # Apply transformation to each user document in the list
            return [UserEntityTransformer.user_entity(item) for item in entity]
        except Exception as e:
            # Log any error during bulk transformation
            logger.error("Error processing user items from MongoDB: %s", str(e))
            raise HTTPException(
                status_code=500,
                detail="Failed to process user items from MongoDB!"
            ) from e
