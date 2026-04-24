import asyncio
import hashlib
import io
import uuid
import filetype
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from urllib.parse import quote
from typing import List, Optional
from pathlib import Path


from api.schemas.item import ItemCreate, FolderContentResponse, ItemResponse, FileResponse as FileResponseSchema, FolderResponse
from models.item import ItemModel, FileModel, FolderModel, ChunkInfo
from core.enums import ItemStatus, ItemType, SharePermission
from core.exceptions import ExistingItemError, ResourceNotFoundError, DataBaseError, ItemIsFolderError, StorageServerError, StorageLimitExceededError, FileTypeNotAllowedError
from core.permissions import verify_access
from core.config import settings
from utils.mappers import map_item_to_response
from gateways.database.repositories.item_repository import item_repository
from gateways.storage.services.node_distribution_service import get_file_from_node, delete_file_from_node
from gateways.storage.services.node_registry import NodeRegistry
from gateways.storage.client.storage_client import StorageClient


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


async def _select_nodes_for_chunks(num_chunks: int) -> list[list[str]]:
    """Returns a list of node_id lists, one per chunk. Rotates the primary node across chunks."""
    assignments = []
    last_primary: list[str] = []
    for _ in range(num_chunks):
        node_ids = await NodeRegistry.select_best_nodes(limit=3, exclude_node_ids=last_primary or None)
        if not node_ids:
            node_ids = await NodeRegistry.select_best_nodes(limit=3)
        if not node_ids:
            return []
        assignments.append(node_ids)
        last_primary = [node_ids[0]]
    return assignments


async def _upload_chunk_to_node(node_id: str, physical_name: str, chunk_size: int, chunk_data: bytes) -> bool:
    try:
        client = StorageClient(node_id=node_id, encryption_key=settings.STORAGE_ENCRYPTION_KEY.encode())
        return await client.upload(physical_name, chunk_size, io.BytesIO(chunk_data))
    except Exception as e:
        print(f"[!] Upload to {node_id} failed: {e}")
        return False


async def _upload_single_chunk(chunk_index: int, chunk_data: bytes, base_uuid: str, node_ids: list[str]) -> ChunkInfo | None:
    physical_name = f"{base_uuid}_{chunk_index}"
    chunk_size = len(chunk_data)
    chunk_hash = hashlib.sha256(chunk_data).hexdigest()

    upload_tasks = [
        _upload_chunk_to_node(node_id, physical_name, chunk_size, chunk_data)
        for node_id in node_ids
    ]
    results = await asyncio.gather(*upload_tasks)
    succeeded_nodes = [node_ids[i] for i, ok in enumerate(results) if ok]

    if not succeeded_nodes:
        print(f"[!] Chunk {chunk_index}: all node uploads failed")
        return None

    return ChunkInfo(
        chunk_index=chunk_index,
        size=chunk_size,
        chunk_hash=chunk_hash,
        physical_name=physical_name,
        node_ids=succeeded_nodes,
    )


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

    file_content = await file.read(settings.MAX_FILE_SIZE_BYTES + 1)
    if len(file_content) > settings.MAX_FILE_SIZE_BYTES:
        raise StorageLimitExceededError
    
    file_size = len(file_content)

    ext = Path(file.filename or "").suffix.lower()
    if ext in settings.BLOCKED_EXTENSIONS:
        raise FileTypeNotAllowedError(ext)

    kind = filetype.guess(file_content[:2048])
    if kind and kind.mime in settings.BLOCKED_MIME_TYPES:
        raise FileTypeNotAllowedError(kind.mime)

    used_bytes = await item_repository.get_used_storage(owner_id)
    if used_bytes + file_size > settings.MAX_STORAGE_BYTES:
        raise StorageLimitExceededError()

    base_uuid = str(uuid.uuid4()).replace("-", "")

    raw_chunks = [
        file_content[i:i + settings.CHUNK_SIZE_BYTES]
        for i in range(0, file_size, settings.CHUNK_SIZE_BYTES)
    ]
    if not raw_chunks:
        raise StorageServerError("Empty file cannot be uploaded")

    chunk_node_assignments = await _select_nodes_for_chunks(len(raw_chunks))
    if not chunk_node_assignments:
        raise StorageServerError("No storage nodes available")

    chunk_tasks = [
        _upload_single_chunk(i, raw_chunks[i], base_uuid, chunk_node_assignments[i])
        for i in range(len(raw_chunks))
    ]
    chunk_results = await asyncio.gather(*chunk_tasks)

    failed = [i for i, r in enumerate(chunk_results) if r is None]
    if failed:
        raise StorageServerError(f"Chunk upload failed for indices: {failed}")

    chunks: list[ChunkInfo] = list(chunk_results)

    combined = "".join(c.chunk_hash for c in chunks)
    file_hash = hashlib.sha256(combined.encode()).hexdigest()

    update_data = {
        "size": file_size,
        "file_type": file.content_type,
        "status": ItemStatus.COMPLETED.value,
        "file_hash": file_hash,
        "chunks": [c.model_dump() for c in chunks],
    }

    updated_model = await item_repository.update(item_id, update_data)
    if not updated_model:
        raise ResourceNotFoundError("Failed to update item after upload")

    return map_item_to_response(updated_model, current_user_id)


async def get_folder_service(folder_id: str, current_user_id: str) -> FolderContentResponse:
    folder_model = await _get_item_or_404(folder_id)
    children = await item_repository.get_children(folder_id)

    child_responses = [map_item_to_response(child, current_user_id) for child in children]

    breadcrumb = await item_repository.get_ancestors(folder_id)

    return FolderContentResponse(
        folder=map_item_to_response(folder_model, current_user_id),
        children=child_responses,
        breadcrumb=breadcrumb
    )


async def remove_item_service(item_id: str, current_user_id: str):
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "remove", SharePermission.EDITOR)

    if not await item_repository.delete(item_id):
        raise DataBaseError()

    if item.item_type == ItemType.FILE and item.chunks:
        for chunk_info in item.chunks:
            for node_id in chunk_info.node_ids:
                await delete_file_from_node(node_id, chunk_info.physical_name)


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

    if not item.chunks:
        raise StorageServerError("File has no associated chunks")

    ordered_chunks = sorted(item.chunks, key=lambda c: c.chunk_index)

    # Eagerly fetch all chunk data BEFORE creating the StreamingResponse.
    # A StreamingResponse sends HTTP 200 headers immediately, so any exception
    # raised inside the generator after that point cannot be turned into an
    # HTTP error response — causing "Caught handled exception, but response
    # already started." By collecting all bytes first, errors propagate through
    # FastAPI's normal exception handlers and return a proper 500 response.
    file_parts: list[bytes] = []
    for chunk_info in ordered_chunks:
        chunk_gen = None
        for node_id in chunk_info.node_ids:
            try:
                chunk_gen = await get_file_from_node(
                    node_id,
                    chunk_info.physical_name,
                    chunk_info.chunk_hash,
                )
                if chunk_gen:
                    break
            except Exception:
                continue
        if not chunk_gen:
            raise StorageServerError(f"Chunk {chunk_info.chunk_index} unavailable on all replicas")
        async for data in chunk_gen:
            file_parts.append(data)

    return StreamingResponse(
        io.BytesIO(b"".join(file_parts)),
        media_type=item.file_type,
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{quote(item.name)}"}
    )


async def mark_item_as_starred_service(item_id: str, current_user_id: str):
    item = await _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "mark as starred", SharePermission.VIEWER)

    is_starred = current_user_id in (item.starred_by or [])
    await item_repository.update_star(item_id, current_user_id, is_starred)

async def search_items_service(query: str, current_user_id: str) -> list[ItemResponse]:
    items = await item_repository.search(current_user_id, query)
    return [map_item_to_response(item, current_user_id) for item in items]