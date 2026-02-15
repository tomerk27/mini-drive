from fastapi import UploadFile, File, Depends
import os
import uuid
import shutil
from bson import ObjectId
from app.schemas.item import ItemCreate
from app.models.item import ItemModel, FileModel, FolderModel
from app.database import get_collection
from app.core.exceptions import ExistingItemError, ResourceNotFoundError, ItemIsNotExistingError
from app.utils.item_utils import ItemStatus
from app.core.config import settings
from app.utils.mappers import map_item_to_response
from app.models.user import User

async def init_item(
    item_data: ItemCreate,
    current_user_id: str
) -> ItemModel:
    items = get_collection('items')

    if await items.find_one({"owner_id": str(current_user_id), "parent_id": item_data.parent_id, "name": item_data.name}):
        raise ExistingItemError(item_data.name)

    item_dict = item_data.model_dump()
    item_dict["owner_id"] = str(current_user_id)
    if item_data.item_type == "FILE":
        item_in_db = FileModel(**item_dict)
    
    else:
        item_in_db = FolderModel(**item_dict)

    item_dict = item_in_db.model_dump(by_alias=True, exclude="_id")

    result = await items.insert_one(item_dict)
    item_in_db.id = result.inserted_id

    return map_item_to_response(item_in_db, current_user_id)

async def complete_item_upload(
    item_id: str,
    owner_id: str,
    file: UploadFile,
    current_user_id: User
) -> ItemModel:
    items = get_collection('items')
    
    try:
        obj_id = ObjectId(item_id)
    except: 
        raise ResourceNotFoundError("Invalid ID format")

    item = await items.find_one({"_id": obj_id, "owner_id": owner_id, "status": ItemStatus.PENDING})

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
    
    except e:
        raise e

    result = await items.find_one_and_update(
        {"_id": obj_id, "owner_id": owner_id, "status": ItemStatus.PENDING},
        {"$set":{
            "physical_path": physical_path,
            "size": file_size,
            "file_type": file_type,
            "status": ItemStatus.COMPLETED
        }},
        return_document=True
    )

    if not result:
        raise ResourceNotFoundError("Pending file not found")

    return map_item_to_response(ItemModel(**result), current_user_id)

async def get_folder_service(folder_id: str, current_user_id: User):
    items = get_collection('items')

    try: 
        ObjectId(folder_id)
    except:
        raise ResourceNotFoundError("Invalid ID format")
    
    folder = await items.find_one({"_id": folder_id})

    if not folder:
        raise ItemIsNotExistingError()
    
    return map_item_to_response(folder, current_user_id)