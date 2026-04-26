import hashlib
import io
import uuid
import filetype
from concurrent.futures import ThreadPoolExecutor
from fastapi.responses import Response
from urllib.parse import quote
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


def _get_item_or_404(item_id: str) -> ItemModel:
    item = item_repository.get_by_id(item_id)
    if not item:
        raise ResourceNotFoundError("Item not found")
    return item


def init_item(item_data: ItemCreate, current_user_id: str) -> ItemResponse:
    if item_repository.get_by_name_and_parent(str(current_user_id), item_data.parent_id, item_data.name):
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

    inserted_id = item_repository.insert(item_in_db)
    item_in_db.id = inserted_id

    return map_item_to_response(item_in_db, current_user_id)



def _upload_chunk_to_node(node_id: str, physical_name: str, chunk_size: int, chunk_data: bytes) -> bool:
    try:
        client = StorageClient(node_id=node_id, encryption_key=settings.STORAGE_ENCRYPTION_KEY.encode())
        return client.upload(physical_name, chunk_size, io.BytesIO(chunk_data))
    except Exception as e:
        print(f"[!] Upload to {node_id} failed: {e}")
        return False


def _upload_single_chunk(chunk_index: int, chunk_data: bytes, base_uuid: str, node_ids: list[str]) -> ChunkInfo | None:
    physical_name = f"{base_uuid}_{chunk_index}"
    chunk_size = len(chunk_data)
    chunk_hash = hashlib.sha256(chunk_data).hexdigest()

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(_upload_chunk_to_node, node_id, physical_name, chunk_size, chunk_data)
            for node_id in node_ids
        ]
        results = [f.result() for f in futures]

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


def complete_item_upload(
    item_id: str,
    owner_id: str,
    file_obj,
    filename: str,
    content_type: str,
    current_user_id: str
) -> ItemResponse:
    item = _get_item_or_404(item_id)
    verify_access(item.model_dump(), owner_id, "upload", SharePermission.OWNER)

    if item.status != ItemStatus.PENDING:
        raise ResourceNotFoundError("Pending file not found")

    ext = Path(filename or "").suffix.lower()
    if ext in settings.BLOCKED_EXTENSIONS:
        raise FileTypeNotAllowedError(ext)

    # Read header once for MIME detection, then stream the rest chunk by chunk
    header = file_obj.read(2048)
    if not header:
        raise StorageServerError("Empty file cannot be uploaded")

    kind = filetype.guess(header)
    if kind and kind.mime in settings.BLOCKED_MIME_TYPES:
        raise FileTypeNotAllowedError(kind.mime)
    mime = kind.mime if kind else (content_type or "application/octet-stream")

    used_bytes = item_repository.get_used_storage(owner_id)
    base_uuid = str(uuid.uuid4()).replace("-", "")

    chunks: list[ChunkInfo] = []
    file_size = 0
    last_primary: list[str] = []

    # Prepend the header bytes back into the first chunk read
    leftover = header
    while True:
        needed = settings.CHUNK_SIZE_BYTES - len(leftover)
        new_data = file_obj.read(needed) if needed > 0 else b""
        chunk_data = leftover + new_data
        leftover = b""

        if not chunk_data:
            break

        file_size += len(chunk_data)

        if file_size > settings.MAX_FILE_SIZE_BYTES:
            raise StorageLimitExceededError()
        if used_bytes + file_size > settings.MAX_STORAGE_BYTES:
            raise StorageLimitExceededError()

        node_ids = NodeRegistry.select_best_nodes(limit=3, exclude_node_ids=last_primary or None)
        if not node_ids:
            node_ids = NodeRegistry.select_best_nodes(limit=3)
        if not node_ids:
            raise StorageServerError("No storage nodes available")

        chunk_index = len(chunks)
        result = _upload_single_chunk(chunk_index, chunk_data, base_uuid, node_ids)
        if result is None:
            raise StorageServerError(f"Chunk {chunk_index} upload failed")

        chunks.append(result)
        last_primary = [node_ids[0]]

        # If the read returned less than a full chunk, we've reached EOF
        if len(chunk_data) < settings.CHUNK_SIZE_BYTES:
            break

    if not chunks:
        raise StorageServerError("Empty file cannot be uploaded")

    combined = "".join(c.chunk_hash for c in chunks)
    file_hash = hashlib.sha256(combined.encode()).hexdigest()

    update_data = {
        "size": file_size,
        "file_type": mime,
        "status": ItemStatus.COMPLETED.value,
        "file_hash": file_hash,
        "chunks": [c.model_dump() for c in chunks],
    }

    updated_model = item_repository.update(item_id, update_data)
    if not updated_model:
        raise ResourceNotFoundError("Failed to update item after upload")

    return map_item_to_response(updated_model, current_user_id)


def get_folder_service(folder_id: str, current_user_id: str) -> FolderContentResponse:
    folder_model = _get_item_or_404(folder_id)
    children = item_repository.get_children(folder_id)

    child_responses = [map_item_to_response(child, current_user_id) for child in children]

    breadcrumb = item_repository.get_ancestors(folder_id)

    return FolderContentResponse(
        folder=map_item_to_response(folder_model, current_user_id),
        children=child_responses,
        breadcrumb=breadcrumb
    )


def remove_item_service(item_id: str, current_user_id: str):
    item = _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "remove", SharePermission.EDITOR)

    if not item_repository.delete(item_id):
        raise DataBaseError()

    if item.item_type == ItemType.FILE and item.chunks:
        for chunk_info in item.chunks:
            for node_id in chunk_info.node_ids:
                delete_file_from_node(node_id, chunk_info.physical_name)


def rename_item_service(item_id: str, current_user_id: str, new_name: str):
    item = _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "rename", SharePermission.EDITOR)

    if not item_repository.update(item_id, {"name": new_name}):
        raise DataBaseError()


def get_file_preview_service(item_id: str, current_user_id: str):
    item = _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "preview", SharePermission.VIEWER)

    if item.item_type == ItemType.FOLDER:
        raise ItemIsFolderError()

    if not item.chunks:
        raise StorageServerError("File has no associated chunks")

    ordered_chunks = sorted(item.chunks, key=lambda c: c.chunk_index)

    file_parts: list[bytes] = []
    for chunk_info in ordered_chunks:
        chunk_data = None
        for node_id in chunk_info.node_ids:
            try:
                chunk_data = get_file_from_node(node_id, chunk_info.physical_name, chunk_info.chunk_hash)
                if chunk_data:
                    break
            except Exception:
                continue
        if not chunk_data:
            raise StorageServerError(f"Chunk {chunk_info.chunk_index} unavailable on all replicas")
        file_parts.append(chunk_data)

    return Response(
        content=b"".join(file_parts),
        media_type=item.file_type,
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{quote(item.name)}"}
    )


def mark_item_as_starred_service(item_id: str, current_user_id: str):
    item = _get_item_or_404(item_id)
    verify_access(item.model_dump(), current_user_id, "mark as starred", SharePermission.VIEWER)

    is_starred = current_user_id in (item.starred_by or [])
    item_repository.update_star(item_id, current_user_id, is_starred)


def search_items_service(query: str, current_user_id: str) -> list[ItemResponse]:
    items = item_repository.search(current_user_id, query)
    return [map_item_to_response(item, current_user_id) for item in items]
