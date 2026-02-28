from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.utils.item_utils import ItemType, ItemStatus
from app.utils.db_utils import PyObjectId
from app.utils.time import current_time

class ItemModel(BaseModel): 
    id: PyObjectId = Field(None, alias='_id')

    owner_id: str = Field(...)
    name: str
    item_type: ItemType

    parent_id: Optional[str] = Field(None)

    created_at: datetime = Field(default_factory=current_time)

    starred_by: List[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class FileModel(ItemModel):
    item_type: ItemType = ItemType.FILE

    file_type: Optional[str] = None
    size: Optional[int] = None
    physical_path: Optional[str] = None

    status: ItemStatus = ItemStatus.PENDING 

class FolderModel(ItemModel):
    item_type: ItemType = ItemType.FOLDER