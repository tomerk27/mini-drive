from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.database import get_users_collection
from app.utils.security import get_password_hash
from app.models.user import User

async def register_new_user(user_data: UserCreate):
    users_collection = get_users_collection()

    existing_user = await users_collection.find_one({"email": user_data.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)

    user_in_db = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
        )
    
    user_dict = user_in_db.model_dump(by_alias=True, exclude=["id"])
    result = await users_collection.insert_one(user_dict)
    user_in_db.id = str(result.inserted_id)

    return UserResponse.model_validate(user_in_db)