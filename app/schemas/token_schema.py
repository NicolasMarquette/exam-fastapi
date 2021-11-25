"""Schemas for the token."""

from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    """Base model for the token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for the data in the token."""
    username: Optional[str] = None
    scopes: List[str] = []

