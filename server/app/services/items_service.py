from fastapi import UploadFile
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from bson import ObjectId
from app.schemas.item import ItemCreate, FolderContentResponse
from app.models.item import ItemModel, FileModel, FolderModel
from app.database import get_collection
from app.core.exceptions import ExistingItemError, ResourceNotFoundError, ItemIsNotExistError, PremissionError, DataBaseError, ItemIsFolderError
from app.utils.item_utils import ItemStatus, ItemType
from app.core.config import settings
from app.utils.mappers import map_item_to_response

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
) -> ItemModel:
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
) -> ItemModel:
    items = get_collection('items')
    
    try:
        obj_id = ObjectId(item_id)
    except: 
        raise ResourceNotFoundError("Invalid ID format")

    item = await items.find_one({
        "_id": obj_id, 
        "owner_id": owner_id, 
        "status": ItemStatus.PENDING.value
        })

    if not item:
        raise ResourceNotFoundError("Pending file not found")

    os.makedirs(settings.files_dir, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1]
    physical_filename = f"{uuid.uuid4()}{file_ext}"
    physical_path = os.path.join(settings.files_dir, physical_filename)

    try: 
        with open(physical_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(physical_path)
        file_type = file.content_type
    
    except Exception as e:
        raise e

    result_dict = await items.find_one_and_update(
        {
            "_id": obj_id,
            "owner_id": owner_id, 
            "status": ItemStatus.PENDING.value
            },
        {"$set":{
            "physical_path": physical_path,
            "size": file_size,
            "file_type": file_type,
            "status": ItemStatus.COMPLETED.value
        }},
        return_document=True
    )

    if not result_dict:
        raise ResourceNotFoundError("Pending file not found")

    updated_model = parse_item_to_model(result_dict)

    return map_item_to_response(updated_model, current_user_id)

async def get_folder_service(folder_id: str, current_user_id: str):
    items = get_collection('items')

    try: 
        obj_id = ObjectId(folder_id)
    except Exception:
        raise ResourceNotFoundError("Invalid ID format")
    
    folder_dict = await items.find_one({"_id": obj_id})

    if not folder_dict:
        raise ItemIsNotExistError()
    
    cursor = items.find({"parent_id": folder_id})
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

    try: 
        obj_id = ObjectId(item_id)
    except Exception:
        raise ResourceNotFoundError("Invalid ID format")
    
    item_to_remove = await items.find_one({'_id': obj_id})

    if not item_to_remove:
        raise ItemIsNotExistError()
    if item_to_remove.get('owner_id') != current_user_id:
        raise PremissionError(action='remove')
    
    physical_path = item_to_remove.get('physical_path')

    try:
        removed = await items.delete_one({'_id': obj_id})

        if removed.deleted_count == 0:
            raise ResourceNotFoundError("The content didn't found")
    except Exception:
        raise DataBaseError()
    
    if item_to_remove.get('item_type') == ItemType.FILE:
        try:
            if physical_path and os.path.exists(physical_path):
                os.remove(physical_path)
        except Exception as e:
            print(f"Failed to delete physical file: {e}")
            raise e
        
async def rename_item_service(item_id: str, current_user_id: str, new_name: str):
    items = get_collection("items")

    try: 
        obj_id = ObjectId(item_id)
    except Exception:
        raise ResourceNotFoundError("Invalid ID format")
    
    item_to_rename = await items.find_one({'_id': obj_id})

    if not item_to_rename:
        raise ItemIsNotExistError()
    if item_to_rename.get('owner_id') != current_user_id:
        raise PremissionError(action='rename')
    
    try:
        renamed = await items.update_one(
            {'_id': obj_id},
            {'$set': {'name': new_name}}
        )

        if renamed.matched_count == 0:
            raise ResourceNotFoundError("The content didn't found")
        
    except Exception:
        raise DataBaseError()
    
async def get_file_preview_service(item_id: str, current_user_id: str):
    items = get_collection("items")

    try: 
        obj_id = ObjectId(item_id)
    except Exception:
        raise ResourceNotFoundError("Invalid ID format")
    
    item = await items.find_one({'_id': obj_id})

    if not item:
        raise ItemIsNotExistError()
    if item.get('owner_id') != current_user_id:
        raise PremissionError(action='preview')
    if item.get('item_type') == ItemType.FOLDER:
        raise ItemIsFolderError()
    
    return FileResponse(
        path=item.get('physical_path'),
        media_type=item.get('file_type'),
        filename=item.get('name')
    )