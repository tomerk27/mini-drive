from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.item_utils import ItemType

class BaseItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    parent_id: Optional[str] = Field(None)

class ItemCreate(BaseItem):
    item_type: ItemType

class FileCreate(ItemCreate):
    item_type: ItemType = ItemType.FILE
    file_type: Optional[str] = None
    size: Optional[int] = 0

class FolderCreate(ItemCreate): 
    item_type: ItemType = ItemType.FOLDER

class ItemResponse(BaseItem): 
    id: str
    created_at: datetime
    is_owner: bool

    class Config:
        populate_by_name = True
        from_attributes = True

class FileResponse(ItemResponse):
    file_type: Optional[str] = None
    size: Optional[int] = None
    item_type: ItemType = ItemType.FILE

class FolderResponse(ItemResponse):
    item_type: ItemType = ItemType.FOLDER