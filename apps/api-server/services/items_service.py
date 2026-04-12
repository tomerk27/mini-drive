from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from urllib.parse import quote
import os
import uuid
from typing import List, Optional

from api.schemas.item import ItemCreate, FolderContentResponse, ItemResponse, FileResponse as FileResponseSchema, FolderResponse
from models.item import ItemModel, FileModel, FolderModel
from core.enums import ItemStatus, ItemType, SharePermission
from core.exceptions import ExistingItemError, ResourceNotFoundError, DataBaseError, ItemIsFolderError, StorageServerError
from core.permissions import verify_access
from core.config import settings
from utils.mappers import map_item_to_response
from infrastructure.database.repositories.item_repository import item_repository
from infrastructure.storage.services.node_distribution_service import send_file_to_nodes, get_file_from_node, delete_file_from_node
from infrastructure.storage.services.node_registry import NodeRegistry


async def _get_item_or_404(item_id: str) -> ItemModel:
    item = await item_repository.get_by_id(item_id)
    if not item:
        raise ResourceNotFoundError("Item not found")
    return item


def parse_item_to_model(raw_dict: dict) -> ItemModel:
    """Converts a raw MongoDB document into the appropriate ItemModel subclass."""
    raw_dict["id"] = str(raw_dict["_id"])
    item_type = raw_dict.get("item_type")
    if item_type == ItemType.FILE:
        return FileModel(**raw_dict)
    elif item_type == ItemType.FOLDER:
        return FolderModel(**raw_dict)
    return ItemModel(**raw_dict)


async def init_item(item_data: ItemCreate, current_user_id: str) -> ItemResponse:
    if await item_repository.get_by_name_and_parent(str(current_user_id), item_data.parent_id, item_data.name):
        raise ExistingItemError(item_data.name)

    if item_data.item_type == ItemType.FILE:
        item_in_db = FileModel(
            **item_data.model_dump(),
            owner_id=str(current_user_id),
            status=ItemStatus.PENDING
        )
    else:
        item_in_db = FolderModel(
            **item_data.model_dump(),
            owner_id=str(current_user_id)
        )

    inserted_id = await item_repository.insert(item_in_db)
    item_in_db.id = inserted_id

    return map_item_to_response(item_in_db, current_user_id)


async def complete_item_upload(
    item_id: str,
    owner_id: str,
    file: UploadFile,
    current_user_id: str
) -> ItemResponse:
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), owner_id, "upload", SharePermission.OWNER)

    if item.status != ItemStatus.PENDING:
        raise ResourceNotFoundError("Pending file not found")

    file_ext = os.path.splitext(file.filename)[1]
    physical_filename = f"{uuid.uuid4()}{file_ext}"

    file_content = await file.read()
    file_size = len(file_content)
    await file.seek(0)

    node_id_list = await NodeRegistry.select_best_nodes()
    if not node_id_list:
        raise StorageServerError("No storage nodes available")

    success, file_hash = await send_file_to_nodes(node_id_list, physical_filename, file_size, file)

    if not success:
        raise StorageServerError("Failed to save to storage nodes")

    update_data = {
        "physical_name": physical_filename,
        "size": file_size,
        "file_type": file.content_type,
        "status": ItemStatus.COMPLETED.value,
        "file_hash": file_hash,
        "node_ids": node_id_list
    }

    updated_model = await item_repository.update(item_id, update_data)
    if not updated_model:
        raise ResourceNotFoundError("Failed to update item after upload")

    return map_item_to_response(updated_model, current_user_id)


async def get_folder_service(folder_id: str, current_user_id: str) -> FolderContentResponse:
    folder_model = await _get_item_or_404(folder_id)
    children = await item_repository.get_children(folder_id)

    child_files = []
    child_folders = []

    for child in children:
        child_response = map_item_to_response(child, current_user_id)
        if child.item_type == ItemType.FILE:
            child_files.append(child_response)
        elif child.item_type == ItemType.FOLDER:
            child_folders.append(child_response)

    return FolderContentResponse(
        folder=map_item_to_response(folder_model, current_user_id),
        child_files=child_files,
        child_folders=child_folders
    )


async def remove_item_service(item_id: str, current_user_id: str):
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "remove", SharePermission.EDITOR)

    if not await item_repository.delete(item_id):
        raise DataBaseError()

    if item.item_type == ItemType.FILE and hasattr(item, 'physical_name') and item.physical_name:
        for node_id in item.node_ids:
            await delete_file_from_node(node_id, item.physical_name)


async def rename_item_service(item_id: str, current_user_id: str, new_name: str):
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "rename", SharePermission.EDITOR)

    if not await item_repository.update(item_id, {"name": new_name}):
        raise DataBaseError()


async def get_file_preview_service(item_id: str, current_user_id: str):
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "preview", SharePermission.VIEWER)

    if item.item_type == ItemType.FOLDER:
        raise ItemIsFolderError()

    if not item.node_ids:
        raise StorageServerError("File has no associated storage nodes")

    file_generator = await get_file_from_node(item.node_ids[0], item.physical_name, item.file_hash)

    if not file_generator:
        raise StorageServerError("File not found on storage server")

    return StreamingResponse(
        file_generator,
        media_type=item.file_type,
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{quote(item.name)}"}
    )


async def mark_item_as_starred_service(item_id: str, current_user_id: str):
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "mark as starred", SharePermission.VIEWER)

    is_starred = current_user_id in (item.starred_by or [])
    await item_repository.update_star(item_id, current_user_id, is_starred)
