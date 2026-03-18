from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId
from app.core.config import settings
from app.models.user import User
from app.core.exceptions import TokenCredentialsError
from app.database import get_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise TokenCredentialsError

    except JWTError:
        raise TokenCredentialsError

    user_collection = get_collection("users")

    user_data = await user_collection.find_one({"_id": ObjectId(user_id)})

    if user_data is None:
        raise TokenCredentialsError
    
    user_data["_id"] = str(user_data["_id"])
    
    return User(**user_data)
