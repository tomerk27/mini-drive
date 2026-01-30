from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from jose import jwt
from typing import Optional
from dotenv import load_dotenv
import os
from app.core.config import settings

load_dotenv()

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
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    data_copy.update({"exp": expire_time})

    encoded_jwt = jwt.encode(data_copy, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt