from fastapi import UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from urllib.parse import quote
import os
import uuid
from bson import ObjectId
from app.schemas.item import ItemCreate, FolderContentResponse, ItemResponse, FileResponse as FileResponseSchema, FolderResponse
from app.models.item import ItemModel, FileModel, FolderModel
from app.database import get_collection
from app.core.exceptions import ExistingItemError, ResourceNotFoundError, DataBaseError, ItemIsFolderError, StorageServerError
from app.utils.item_utils import ItemStatus, ItemType, SharePermission,get_item_or_404, verify_access
from app.core.config import settings
from app.utils.mappers import map_item_to_response, map_items_to_responses
from app.services.storage_service import send_file_to_storage, get_file_from_storage, delete_file_from_storage

def parse_item_to_model(raw_dict: dict) -> ItemModel:
    item_type = raw_dict.get("item_type")
    
    if item_type == ItemType.FILE:
        return FileModel(**raw_dict)
    elif item_type == ItemType.FOLDER:
        return FolderModel(**raw_dict)
    else:
        return ItemModel(**raw_dict)

async def init_item(
    item_data: ItemCreate,
    current_user_id: str
) -> ItemResponse:
    items = get_collection('items')

    if await items.find_one({"owner_id": str(current_user_id), "parent_id": item_data.parent_id, "name": item_data.name}):
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

    item_dict_for_db = item_in_db.model_dump(by_alias=True, exclude={"id"})

    result = await items.insert_one(item_dict_for_db)
    
    item_in_db.id = str(result.inserted_id)

    return map_item_to_response(item_in_db, current_user_id)

async def complete_item_upload(
    item_id: str,
    owner_id: str,
    file: UploadFile,
    current_user_id: str
) -> ItemResponse:
    items = get_collection('items')
    
    # We verify the pending item exists and belongs to the owner
    item = await get_item_or_404(item_id)
    verify_access(item, owner_id, "upload", SharePermission.OWNER)
    
    if item.get("status") != ItemStatus.PENDING.value:
        raise ResourceNotFoundError("Pending file not found")

    file_ext = os.path.splitext(file.filename)[1]
    physical_filename = f"{uuid.uuid4()}{file_ext}"

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    success, file_hash = send_file_to_storage(physical_filename, file_size, file.file)
    
    if not success:
        raise StorageServerError("Failed to save to storage node")

    result_dict = await items.find_one_and_update(
        {
            "_id": ObjectId(item_id),
            "owner_id": owner_id, 
            "status": ItemStatus.PENDING.value
            },
        {"$set":{
            "physical_name": physical_filename,
            "size": file_size,
            "file_type": file.content_type,
            "status": ItemStatus.COMPLETED.value,
            "file_hash": file_hash
        }},
        return_document=True
    )

    if not result_dict:
        raise ResourceNotFoundError("Pending file not found")

    updated_model = parse_item_to_model(result_dict)

    return map_item_to_response(updated_model, current_user_id)

async def get_folder_service(folder_id: str, current_user_id: str):
    items_collection = get_collection('items')

    folder_dict = await get_item_or_404(folder_id)
    
    cursor = items_collection.find({"parent_id": folder_id})
    children_dicts = await cursor.to_list(length=1000)

    child_files = []
    child_folders = []

    for child_dict in children_dicts:
        child_model = parse_item_to_model(child_dict)
        child_response = map_item_to_response(child_model, current_user_id)
        
        if child_dict.get("item_type") == ItemType.FILE:
            child_files.append(child_response)
        elif child_dict.get("item_type") == ItemType.FOLDER:
            child_folders.append(child_response)

    folder_model = parse_item_to_model(folder_dict)
    
    return FolderContentResponse(
        folder=map_item_to_response(folder_model, current_user_id),
        child_files=child_files,
        child_folders=child_folders
    )

async def remove_item_service(item_id: str, current_user_id: str):
    items = get_collection("items")

    item_to_remove = await get_item_or_404(item_id)
    verify_access(item_to_remove, current_user_id, "remove", SharePermission.EDITOR)
    
    physical_name = item_to_remove.get('physical_name')

    try:
        await items.delete_one({'_id': ObjectId(item_id)})
    except Exception:
        raise DataBaseError()
    
    if item_to_remove.get('item_type') == ItemType.FILE and physical_name:
        delete_file_from_storage(physical_name)
        
async def rename_item_service(item_id: str, current_user_id: str, new_name: str):
    items = get_collection("items")

    item_to_rename = await get_item_or_404(item_id)
    verify_access(item_to_rename, current_user_id, "rename", SharePermission.EDITOR)
    
    try:
        await items.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {'name': new_name}}
        )
    except Exception:
        raise DataBaseError()
    
async def get_file_preview_service(item_id: str, current_user_id: str):
    item = await get_item_or_404(item_id)
    verify_access(item, current_user_id, "preview", SharePermission.VIEWER)

    if item.get('item_type') == ItemType.FOLDER:
        raise ItemIsFolderError()
    
    physical_name = item.get('physical_name')
    file_type = item.get('file_type')
    name = item.get('name')
    file_hash = item.get('file_hash')
    
    file_generator = get_file_from_storage(physical_name, file_hash)

    if not file_generator:
        raise StorageServerError("File not found on storage server")
    
    return StreamingResponse(
        file_generator,
        media_type=file_type,
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{quote(name)}"}
    )

async def mark_item_as_starred_service(item_id: str, current_user_id: str):
    items = get_collection("items")

    item_to_mark = await get_item_or_404(item_id)
    verify_access(item_to_mark, current_user_id, "mark as starred", SharePermission.VIEWER)

    current_stars = item_to_mark.get("starred_by", [])
    update_op = {"$pull": {"starred_by": current_user_id}} if current_user_id in current_stars else {"$addToSet": {"starred_by": current_user_id}}

    try:
        await items.update_one({'_id': ObjectId(item_id)}, update_op)
    except Exception:
        raise DataBaseError()