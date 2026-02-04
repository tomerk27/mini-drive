from app.models.item import ItemModel
from app.models.user import User
from app.schemas.item import ItemResponse

def map_item_to_response(item_db: ItemModel, current_user: User) -> ItemResponse:
    item_dict = item_db.model_dump(by_alias=True)

    item_dict["id"] = str(item_db.id)
    item_dict["is_owner"] = (item_db.owner_id == current_user.id)

    return ItemResponse(**item_dict)