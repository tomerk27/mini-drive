from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel): 
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: str

class UserResponse(UserBase):
    username: str
    id: Optional[str] = Field(None, alias='_id')
    created_at: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read data from object attributes
        populate_by_name = True

class UserLogin(UserBase):
    password: str

class Token(BaseModel): 
    access_token: str
    token_type: str