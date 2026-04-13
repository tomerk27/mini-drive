from core.config import settings
from api.schemas.user import UserCreate, UserLogin, UserResponse
from api.schemas.item import FolderCreate
from gateways.database.repositories.user_repository import user_repository
from core.security import get_password_hash, verify_password, create_access_token
from models.user import User
from core.exceptions import UserNotFoundError, ExistingUserError
from services.items_service import init_item


async def register_new_user(user_data: UserCreate):
    existing_user = await user_repository.get_by_email(user_data.email)
    if existing_user:
        raise ExistingUserError()

    hashed_password = get_password_hash(user_data.password)

    user_in_db = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    user_id = await user_repository.insert(user_in_db)
    user_in_db.id = user_id

    root_folder = await init_item(FolderCreate(name='root'), user_in_db.id)

    await user_repository.update(user_id, {"root_id": root_folder.id})

    return UserResponse(
        access_token=create_access_token(data={"sub": user_in_db.id, "root_folder_id": root_folder.id}),
        token_type="bearer",
    )


async def login_user(user_data: UserLogin):
    user_doc = await user_repository.get_by_email(user_data.email)
    if not user_doc:
        raise UserNotFoundError()

    if verify_password(user_data.password, user_doc.hashed_password):
        return UserResponse(
            access_token=create_access_token(data={
                "sub": str(user_doc.id),
                "root_folder_id": str(user_doc.root_id)
            }),
            token_type=settings.TOKEN_TYPE,
        )

    raise UserNotFoundError()
