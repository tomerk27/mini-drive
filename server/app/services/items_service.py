from fastapi import UploadFile, File
import os
import uuid
import shutil
from bson import ObjectId
from app.schemas.item import BaseItem
from app.models.item import ItemModel
from app.database import get_collection
from app.core.exceptions import ExistingItemError, ResourceNotFoundError
from app.utils.item_utils import ItemStatus
from app.core.config import settings

async def init_item(
    item_data: BaseItem,
    owner_id: str,
) -> ItemModel:
    items = get_collection('items')

    if await items.find_one({"owner_id": owner_id, "parent_id": item_data.parent_id, "name": item_data.name}):
        raise ExistingItemError

    item_in_db = ItemModel(owner_id, **item_data)

    item_dict = item_in_db.model_dump(by_alias=True, exclude="_id")

    result = await items.insert_one(item_dict)
    item_in_db.id = result.inserted_id

    return map_item_to_response(item_in_db, )

async def complete_item_upload(
    item_id: str,
    owner_id: str,
    file: UploadFile
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
    physical_path = os.path.join(setting.files_dir, physical_filename)

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
            "size": size,
            "file_type": file_type,
            "status": ItemStatus.COMPLETED
        }},
        return_document=True
    )

    if not result:
        raise ResourceNotFoundError("Pending file not found")

    return ItemModel(**result)