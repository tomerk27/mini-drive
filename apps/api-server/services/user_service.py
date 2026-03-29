from infrastructure.database.database import get_collection
from api.schemas.item_pages import ItemPageResponse
from services.items_service import parse_item_to_model
from utils.mappers import map_items_to_responses
from core.exceptions import ResourceNotFoundError

async def get_starred_items_service(current_user_id: str):
    responses = await _fetch_and_process_items(
        {"starred_by": current_user_id}, 
        current_user_id
    )
    return ItemPageResponse(items=responses)


async def get_shared_items_service(current_user_id: str):
    responses = await _fetch_and_process_items(
        {"shared_with.id": current_user_id}, 
        current_user_id
    )
    return ItemPageResponse(items=responses)

async def _fetch_and_process_items(query_filter: dict, current_user_id: str):
    items_collection = get_collection("items")

    cursor = items_collection.find(query_filter)
    items_dicts = await cursor.to_list(length=100)

    if not items_dicts:
        raise ResourceNotFoundError()

    items_models = [parse_item_to_model(d) for d in items_dicts]
    items_responses = map_items_to_responses(items_models, current_user_id)
    
    return items_responses