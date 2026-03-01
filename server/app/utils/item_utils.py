from enum import Enum
from bson import ObjectId
from app.database import get_collection
from app.core.exceptions import ResourceNotFoundError, ItemIsNotExistError, PremissionError

class ItemType(str, Enum):
    FOLDER = "folder"
    FILE = "file"

class ItemStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

async def get_item_or_404(item_id: str) -> dict:
    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise ResourceNotFoundError("Invalid ID format")

    item = await get_collection("items").find_one({"_id": obj_id})
    if not item:
        raise ItemIsNotExistError()
    return item

def verify_ownership(item: dict, user_id: str, action: str):
    if item.get("owner_id") != user_id:
        raise PremissionError(action=action)