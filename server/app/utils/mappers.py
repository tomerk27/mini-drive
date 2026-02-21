from app.models.item import ItemModel
from app.schemas.item import FolderResponse, FileResponse, ItemResponse

def map_item_to_response(item_db: ItemModel, current_user_id: str) -> ItemResponse:
    item_dict = item_db.model_dump(by_alias=True)

    if "_id" in item_dict and item_dict["_id"]:
        item_dict["id"] = str(item_dict["_id"])
        del item_dict["_id"]
    elif hasattr(item_db, "id") and item_db.id:
        item_dict["id"] = str(item_db.id)

    item_dict["is_owner"] = (item_db.owner_id == current_user_id)

    if item_db.item_type == "FILE":
        return FileResponse(**item_dict)
    elif item_db.item_type == "FOLDER":
        return FolderResponse(**item_dict)
        
    return ItemResponse(**item_dict)