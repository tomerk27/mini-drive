"""
Business logic for user-level views: starred items, shared items, and storage quota.
"""

from bson import ObjectId
from gateways.database.repositories.item_repository import item_repository
from gateways.database.database import get_collection
from api.schemas.item_pages import ItemPageResponse
from api.schemas.user import StorageResponse
from utils.mappers import map_item_to_response, map_items_to_responses
from core.config import settings


def get_starred_items_service(current_user_id: str) -> ItemPageResponse:
    """
    Returns all items the user has starred.

    Args:
        current_user_id: The logged-in user's ID.

    Returns:
        ItemPageResponse with up to 100 starred items.
    """
    items = item_repository.get_starred_items(current_user_id)
    return ItemPageResponse(items=map_items_to_responses(items, current_user_id))


def get_shared_items_service(current_user_id: str) -> ItemPageResponse:
    """
    Returns all items shared with the user by other users.

    Enriches each item response with the owner's username so the UI can
    show "Shared by <username>" without a separate request.

    Args:
        current_user_id: The logged-in user's ID.

    Returns:
        ItemPageResponse with up to 100 shared items.
    """
    items = item_repository.get_shared_items(current_user_id)

    # Batch-fetch all unique owner usernames in one query rather than N+1 queries.
    owner_ids = list({item.owner_id for item in items})
    users_collection = get_collection("users")
    owner_docs = list(users_collection.find(
        {"_id": {"$in": [ObjectId(oid) for oid in owner_ids]}},
        {"_id": 1, "username": 1}
    ))
    owner_username_map = {str(doc["_id"]): doc["username"] for doc in owner_docs}

    responses = [
        map_item_to_response(item, current_user_id, owner_username=owner_username_map.get(item.owner_id))
        for item in items
    ]
    return ItemPageResponse(items=responses)


def get_storage_service(current_user_id: str) -> StorageResponse:
    """
    Returns the user's current storage usage and maximum quota.

    Args:
        current_user_id: The logged-in user's ID.

    Returns:
        StorageResponse with used_bytes and max_bytes.
    """
    used_bytes = item_repository.get_used_storage(current_user_id)
    return StorageResponse(used_bytes=used_bytes, max_bytes=settings.MAX_STORAGE_BYTES)
