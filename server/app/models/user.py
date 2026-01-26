from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str = Field(..., min_length=4)
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Jerusalem")))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example" : {
                "username": "Tomer",
                "email": "tomer@example.com",
                "hashed_password": "...",
            }
        }