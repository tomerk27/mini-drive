"""
Security utilities: password hashing and JWT token creation.
"""

from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from jose import jwt
from typing import Optional
from dotenv import load_dotenv
from core.config import settings

load_dotenv()

# bcrypt context used for hashing and verifying user passwords.
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(origin_password: str, hashed_password: str) -> bool:
    """
    Checks a plain-text password against a stored bcrypt hash.

    Args:
        origin_password: The raw password the user typed.
        hashed_password: The bcrypt hash stored in the database.

    Returns:
        True if the password matches, False otherwise.
    """
    return password_context.verify(origin_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password with bcrypt for safe storage.

    Args:
        password: The raw password to hash.

    Returns:
        A bcrypt-hashed string suitable for storing in the database.
    """
    return password_context.hash(password)


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT access token containing the given payload.

    Args:
        data: Dictionary of claims to embed in the token (e.g. user ID, root folder).
        expire_delta: How long until the token expires. Defaults to
            settings.ACCESS_TOKEN_EXPIRE_MINUTES if not provided.

    Returns:
        A signed JWT string the client should store and send as a Bearer token.
    """
    data_copy = data.copy()

    if expire_delta:
        expire_time = datetime.now(timezone.utc) + expire_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiry claim before signing.
    data_copy.update({"exp": expire_time})

    encoded_jwt = jwt.encode(data_copy, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt