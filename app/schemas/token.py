"""
Schemas for JWT authentication in FastAPI.

This module contains Pydantic models used for validating and serializing JWT
tokens and their data.

Classes:
    Token: Represents the JWT access token response, including the token,
           its type, and user role information.
    TokenData: Represents the decoded JWT token payload, which includes
               the username and granted scopes (permissions).
"""
from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for the JWT access token response.

    Attributes:
        access_token (str): The JWT token.
        token_type (str): The type of token (e.g., 'bearer').
        user_role (dict): The user's role and metadata.
    """
    access_token: str
    token_type: str
    user_name: str


class TokenData(BaseModel):
    """
    Schema for the decoded JWT token payload.

    Attributes:
        username (str | None): The username extracted from the token.
        scopes (list[str]): Scopes or permissions granted to the token.
    """
    username: Optional[str] = None
    scopes: List[str] = []
