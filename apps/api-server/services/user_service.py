from gateways.database.repositories.item_repository import item_repository
from api.schemas.item_pages import ItemPageResponse
from api.schemas.user import StorageResponse
from utils.mappers import map_items_to_responses
from core.config import settings


async def get_starred_items_service(current_user_id: str) -> ItemPageResponse:
    items = await item_repository.get_starred_items(current_user_id)
    return ItemPageResponse(items=map_items_to_responses(items, current_user_id))


async def get_shared_items_service(current_user_id: str) -> ItemPageResponse:
    items = await item_repository.get_shared_items(current_user_id)
    return ItemPageResponse(items=map_items_to_responses(items, current_user_id))


async def get_storage_service(current_user_id: str) -> StorageResponse:
    used_bytes = await item_repository.get_used_storage(current_user_id)
    return StorageResponse(used_bytes=used_bytes, max_bytes=settings.MAX_STORAGE_BYTES)
