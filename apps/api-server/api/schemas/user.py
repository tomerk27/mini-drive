from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel): 
    email: EmailStr

class UserCreate(UserBase):
    username: str = Field(..., min_length=4)
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(BaseModel): 
    access_token: str
    token_type: str