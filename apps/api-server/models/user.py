from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from utils.time import current_time
from core.types import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(None, alias="_id")
    username: str = Field(..., min_length=4)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=current_time)
    root_id: PyObjectId = None

    class Config:
        populate_by_name = True
