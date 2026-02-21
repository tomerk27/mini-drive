from pydantic import BaseModel, EmailStr

class UserBase(BaseModel): 
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(BaseModel): 
    access_token: str
    token_type: str