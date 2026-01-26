from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from jose import jwt
from typing import Optional

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30
TOKEM_TYPE = "bearer"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(origin_password: str, hashed_password: str) -> bool:
    return password_context.verify(origin_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_context.hash(password)

def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    data_copy = data.copy()

    if expire_delta:
        expire_time = datetime.now(timezone.utc) + expire_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)

    data_copy.update({"exp": expire_time})

    encoded_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt