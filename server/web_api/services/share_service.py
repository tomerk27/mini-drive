from bson import ObjectId
from web_api.schemas.share import ShareRequest
from common.utils.item_utils import get_item_or_404, verify_access, SharePermission
from common.database import get_collection
from common.core.exceptions import UserNotFoundError, SelfShareError
from common.models.item import SharedUser


async def share_item_service(share_schema: ShareRequest, item_id, current_user_id):
    users = get_collection("users")
    items = get_collection("items")

    item = await get_item_or_404(item_id)
    verify_access(item, current_user_id, "share item", SharePermission.EDITOR)

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
        {
            "$push": {
                "shared_with": new_share.model_dump()
            }
        },
    )
