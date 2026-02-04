from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from app.utils.time import current_time

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str = Field(..., min_length=4)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=current_time)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example" : {
                "username": "Tomer",
                "email": "tomer@example.com",
                "hashed_password": "...",
            }
        }