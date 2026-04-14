from typing import List, Union
from core.enums import ItemType
from api.schemas.item import FolderResponse, FileResponse, ItemResponse


def map_item_to_response(item_db, current_user_id: str) -> Union[FileResponse, FolderResponse, ItemResponse]:
    """Converts a database model into the appropriate public response schema."""
    item_dict = item_db.model_dump(by_alias=True)

    if "_id" in item_dict and item_dict["_id"]:
        item_dict["id"] = str(item_dict["_id"])
        del item_dict["_id"]
    elif hasattr(item_db, "id") and item_db.id:
        item_dict["id"] = str(item_db.id)

    is_owner = (item_db.owner_id == current_user_id)
    item_dict["is_owner"] = is_owner
    item_dict["shared_with"] = item_dict.get("shared_with", []) if is_owner else []

    if item_db.item_type == ItemType.FILE:
        return FileResponse(**item_dict)
    elif item_db.item_type == ItemType.FOLDER:
        return FolderResponse(**item_dict)

    return ItemResponse(**item_dict)


def map_items_to_responses(item_models: List, current_user_id: str) -> List[Union[FileResponse, FolderResponse, ItemResponse]]:
    """Maps a list of database models to a list of response schemas."""
    return [map_item_to_response(model, current_user_id) for model in item_models]
