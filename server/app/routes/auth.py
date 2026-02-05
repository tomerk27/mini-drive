from fastapi import APIRouter, status
from app.schemas.user import UserResponse, UserCreate, UserLogin, Token
from app.services.auth_service import register_new_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    return await register_new_user(user)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    return await login_user(user)