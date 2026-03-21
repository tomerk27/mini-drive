from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from common import ItemType, SharePermission

class BaseItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    parent_id: Optional[str] = Field(None)

class SharedUserResponse(BaseModel):
    id: str
    permission: SharePermission
    email: Optional[str] = None

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
    item_type: ItemType
    is_owner: bool
    starred_by: List[str]
    shared_with: List[SharedUserResponse] = []

    class Config:
        populate_by_name = True
        from_attributes = True

class FileResponse(ItemResponse):
    file_type: Optional[str] = None
    size: Optional[int] = None
    item_type: ItemType = ItemType.FILE

class FolderResponse(ItemResponse):
    item_type: ItemType = ItemType.FOLDER

class FolderContentResponse(BaseModel):
    folder: FolderResponse

    child_files: List[FileResponse] = []
    child_folders: List[FolderResponse] = []

class ItemRename(BaseModel):
    new_name: str