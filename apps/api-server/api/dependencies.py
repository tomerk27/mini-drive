"""
FastAPI dependency functions injected into route handlers.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId
from core.config import settings
from models.user import User
from core.exceptions import TokenCredentialsError
from gateways.database.database import get_collection

# Tells FastAPI where clients obtain a token (used by the OpenAPI docs).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    FastAPI dependency that validates the Bearer JWT and returns the logged-in user.

    Inject this into any route that requires authentication:
        current_user: User = Depends(get_current_user)

    Args:
        token: JWT extracted automatically from the Authorization header.

    Returns:
        The User object for the authenticated user.

    Raises:
        TokenCredentialsError: If the token is missing, expired, or invalid,
            or if the user no longer exists in the database.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise TokenCredentialsError

    except JWTError:
        raise TokenCredentialsError

    user_collection = get_collection("users")
    user_data = user_collection.find_one({"_id": ObjectId(user_id)})

    if user_data is None:
        raise TokenCredentialsError

    # Convert ObjectId to string so Pydantic can populate the User model.
    user_data["_id"] = str(user_data["_id"])
    return User(**user_data)
