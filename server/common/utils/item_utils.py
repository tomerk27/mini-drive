from enum import Enum
from bson import ObjectId
from common.database import get_collection
from common.core.exceptions import ResourceNotFoundError, ItemIsNotExistError, PermissionError

class ItemType(str, Enum):
    FOLDER = "folder"
    FILE = "file"

class ItemStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class SharePermission(str, Enum): 
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"

async def get_item_or_404(item_id: str) -> dict:
    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise ResourceNotFoundError("Invalid ID format")

    item = await get_collection("items").find_one({"_id": obj_id})
    if not item:
        raise ItemIsNotExistError()
    return item
    
def verify_access(item: dict, user_id: str, action: str, required_permission: SharePermission):
    if item.get("owner_id") == user_id:
        return # The owner can do everything
    
    shared_with = item.get("shared_with", [])

    for user in shared_with:
        user_current_permission = user.get("permission")
        print(user_current_permission)

        if user.get("id") == user_id:
            if required_permission == SharePermission.VIEWER:
                return
            
            if required_permission == SharePermission.EDITOR and user_current_permission == SharePermission.EDITOR:
                return
            
            raise PermissionError(action=action)
        
    raise PermissionError(action=action)