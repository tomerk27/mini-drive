from app.core.config import settings
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.item import FolderCreate
from app.database import get_collection
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.core.exceptions import UserNotFoundError, ExistingUserError
from app.services.items_service import init_item

async def register_new_user(user_data: UserCreate):
    users_collection = get_collection("users")

    existing_user = await users_collection.find_one({"email": user_data.email})

    if existing_user:
        raise ExistingUserError()
    
    hashed_password = get_password_hash(user_data.password)

    user_in_db = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
        

    user_dict = user_in_db.model_dump(by_alias=True, exclude=["id"])
    result = await users_collection.insert_one(user_dict)
    user_in_db.id = str(result.inserted_id)

    root_folder = await init_item(FolderCreate(name='root'), user_in_db.id)

    await users_collection.update_one(
        {"_id": result.inserted_id},
        {"$set": {"root_id": root_folder.id}}
    )

    return UserResponse(
        access_token=create_access_token(data={"sub": user_in_db.id, "root_folder_id": root_folder.id}),
        token_type="bearer",
    )

async def login_user(user_data: UserLogin):
    users_collection = get_collection("users")

    user_doc = await users_collection.find_one({"email": user_data.email})

    if not user_doc: 
        raise UserNotFoundError()

    correct_password = verify_password(user_data.password, user_doc["hashed_password"])

    if correct_password:
        root_folder_id = user_doc["root_id"]
        user_id = str(user_doc["_id"])

        return UserResponse(
            access_token=create_access_token(data= {"sub": user_id, "root_folder_id": root_folder_id}),
            token_type=settings.token_type,
        )
    else:
        raise UserNotFoundError()
        