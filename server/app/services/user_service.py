from app.database import get_collection
from app.schemas.starred_items import StarredItemsResponse
from app.services.items_service import parse_item_to_model
from app.utils.mappers import map_items_to_responses

async def get_starred_items_service(
    current_user_id: str 
):
    items_collection = get_collection("items")

    cursor = items_collection.find({"starred_by": current_user_id})
    starred_items_dicts = await cursor.to_list(length=100)

    starred_items_models = [parse_item_to_model(d) for d in starred_items_dicts]
    
    starred_items_responses = map_items_to_responses(starred_items_models, current_user_id)
    
    return StarredItemsResponse(starred_items=starred_items_responses)