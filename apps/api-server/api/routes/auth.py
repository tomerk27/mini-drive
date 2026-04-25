from fastapi import APIRouter, status
from api.schemas.user import UserCreate, UserLogin, UserResponse
from services.auth_service import register_new_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    return register_new_user(user)

@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(user: UserLogin):
    return login_user(user)
