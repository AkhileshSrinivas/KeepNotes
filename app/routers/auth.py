"""
This module handles authentication-related endpoints for generating access tokens.

It includes an endpoint for validating user credentials using an OAuth2-compatible form
and issuing a JWT access token. The token contains user information such as email, role,
and expiration time, and can be used to access protected resources.

Features:
- Validates credentials with secure password verification.
- Issues JWT access tokens with configurable expiration.

Dependencies:
- AuthService: Handles password verification and token creation.
- UserService: Interacts with user data to retrieve user details.
- Token: A Pydantic model representing the token response.
- OAuth2PasswordRequestForm: Parses username/password for authentication requests.
"""

from datetime import timedelta
import logging
from schemas.token import Token
from services.auth import AuthService
from managers.users import FetchService
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import database
from models.database import User
from schemas.register import UserCreate

# Define the token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 360
auth_router = APIRouter(
    tags=["Authentication"]
)

@auth_router.post("/login_page")
async def generate_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)) -> Token:
    """
    Generate an access token for a valid user.

    This endpoint validates user credentials using the OAuth2PasswordRequestForm,
    retrieves the user's details from the database, and issues a JWT token if the
    credentials are valid. The token can be used to access protected resources.

    Args:
    - form_data (OAuth2PasswordRequestForm): The login credentials (username and password).

    Returns:
    - Token: A Pydantic model containing the access token, its type, and the user's role.

    Raises:
    - HTTPException: If the username does not exist, the password is incorrect, or any
    unexpected error occurs during token generation.
    """

    try:
        # Fetch the user by email (username from the form data)
        print(form_data.username)
        user = await FetchService.get_user_by_email(form_data.username, db)

        if not user:
            raise HTTPException(status_code=400, detail="Invalid username or password!")

        try:
            # Validate the user's password using a secure hash verification method
            if not AuthService.verify_password(form_data.password, user["password"]):
                raise HTTPException(status_code=400, detail="Invalid username or password!")

        except Exception as verify_error:
            raise HTTPException(
                status_code=400,
                detail="Invalid username or password!"
            ) from verify_error  # Explicitly chain the original exception

        print(user["email"])
        # Create the JWT token with expiration
        access_token = await AuthService.create_access_token(
            data={"sub": user["email"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return Token(access_token=access_token, token_type="bearer", user_name=user["name"])

    except HTTPException as http_err:
        # Re-raise HTTPExceptions as is
        raise http_err

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

@auth_router.post("/signup_page", response_model=dict)
def register(new_user: UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user with hashed password."""
    existing = db.query(User).filter(User.user_email == new_user.user_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = AuthService.hash_password(new_user.password)
    user_obj = User(user_name=new_user.user_name, user_email=new_user.user_email, password=hashed_pwd)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"message": "User registered successfully"}
