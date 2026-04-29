"""
Request/response schemas for auth and user endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Shared base with just email — used by both login and registration."""
    email: EmailStr


class UserCreate(UserBase):
    """Request body for POST /auth/register."""
    username: str = Field(..., min_length=4)
    password: str


class UserLogin(UserBase):
    """Request body for POST /auth/login."""
    password: str


class UserResponse(BaseModel):
    """Returned after successful login or registration. Client stores access_token as a Bearer token."""
    access_token: str
    token_type: str


class StorageResponse(BaseModel):
    """Returned by GET /users/storage — shows how much of the 5 GB quota is used."""
    used_bytes: int
    max_bytes: int