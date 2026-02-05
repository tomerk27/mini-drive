from app.models.item import ItemModel
from app.models.user import User
from app.schemas.item import ItemResponse,FileResponse

def map_item_to_response(item_db: ItemModel, current_user: User) -> ItemResponse:
    item_dict = item_db.model_dump(by_alias=True)

    if "_id" in item_dict:
        item_dict["id"] = str(item_dict["_id"])
        del item_dict["_id"]

    item_dict["is_owner"] = (item_db.owner_id == current_user.id)

    if item_dict.get("item_type") == "file":
        return FileResponse(**item_dict)
    elif item_dict.get("item_type") == "folder":
        return FolderResponse(**item_dict)