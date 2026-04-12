from bson import ObjectId
from api.schemas.share import ShareRequest
from core.enums import SharePermission
from core.permissions import verify_access
from core.exceptions import UserNotFoundError, SelfShareError, ResourceNotFoundError
from infrastructure.database.database import get_collection
from infrastructure.database.repositories.item_repository import item_repository
from models.item import SharedUser


async def share_item_service(share_schema: ShareRequest, item_id: str, current_user_id: str):
    users = get_collection("users")
    items = get_collection("items")

    item = await item_repository.get_by_id(item_id)
    if not item:
        raise ResourceNotFoundError("Item not found")

    verify_access(item.model_dump(), current_user_id, "share item", SharePermission.EDITOR)

    user_to_share = await users.find_one({"email": share_schema.email})
    if not user_to_share:
        raise UserNotFoundError()

    user_id_str = str(user_to_share.get("_id"))
    if user_id_str == current_user_id:
        raise SelfShareError

    new_share = SharedUser(
        permission=share_schema.permission,
        id=user_id_str,
        email=user_to_share.get("email")
    )

    await items.update_one(
        {"_id": ObjectId(item_id)},
        {"$push": {"shared_with": new_share.model_dump()}}
    )
