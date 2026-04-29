"""
Pydantic model for a registered CyberDrive user.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from utils.time import current_time
from core.types import PyObjectId


class User(BaseModel):
    """
    Represents a user account as stored in the 'users' MongoDB collection.

    The id field maps to MongoDB's _id (via alias). root_id points to the
    user's top-level root folder, created automatically on registration.
    """
    id: PyObjectId = Field(None, alias="_id")
    username: str = Field(..., min_length=4)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=current_time)
    root_id: PyObjectId = None  # Set after the root folder is created at registration.

    class Config:
        populate_by_name = True
