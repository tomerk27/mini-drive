"""
Business logic for user registration and login.
"""

from core.config import settings
from api.schemas.user import UserCreate, UserLogin, UserResponse
from api.schemas.item import FolderCreate
from gateways.database.repositories.user_repository import user_repository
from core.security import get_password_hash, verify_password, create_access_token
from models.user import User
from core.exceptions import UserNotFoundError, ExistingUserError
from services.items_service import init_item


def register_new_user(user_data: UserCreate) -> UserResponse:
    """
    Creates a new user account and a root folder, then returns a JWT.

    The root folder is created here so the client immediately has a valid
    folder to navigate into after registration.

    Args:
        user_data: The validated registration payload (email, username, password).

    Returns:
        A UserResponse containing the JWT access token.

    Raises:
        ExistingUserError: If the email is already registered.
    """
    existing_user = user_repository.get_by_email(user_data.email)
    if existing_user:
        raise ExistingUserError()

    hashed_password = get_password_hash(user_data.password)

    user_in_db = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    user_id = user_repository.insert(user_in_db)
    user_in_db.id = user_id

    # Every user gets a root folder automatically — it's their top-level drive.
    root_folder = init_item(FolderCreate(name='root'), user_in_db.id)
    user_repository.update(user_id, {"root_id": root_folder.id})

    # Embed the root folder ID in the token so the client can navigate immediately.
    return UserResponse(
        access_token=create_access_token(data={"sub": user_in_db.id, "root_folder_id": root_folder.id}),
        token_type="bearer",
    )


def login_user(user_data: UserLogin) -> UserResponse:
    """
    Validates credentials and returns a JWT on success.

    Args:
        user_data: The validated login payload (email, password).

    Returns:
        A UserResponse containing the JWT access token.

    Raises:
        UserNotFoundError: If the email doesn't exist or the password is wrong.
            (Both cases return the same error to prevent user enumeration.)
    """
    user_doc = user_repository.get_by_email(user_data.email)
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
