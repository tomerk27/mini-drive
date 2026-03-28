from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from common.utils.item_utils import ItemType, SharePermission

class ItemResponse(BaseModel):
    id: str
    name: str
    parent_id: Optional[str]
    item_type: ItemType
    created_at: datetime
    owner_id: str
    is_owner: bool = False
    starred_by: List[str] = []

class FileResponse(ItemResponse):
    item_type: ItemType = ItemType.FILE
    file_type: Optional[str] = None
    size: Optional[int] = None

class FolderResponse(ItemResponse):
    item_type: ItemType = ItemType.FOLDER

class ItemCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None
    item_type: ItemType

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None

class ItemRename(BaseModel):
    name: str

class FolderContentResponse(BaseModel):
    folder: FolderResponse
    child_files: List[FileResponse]
    child_folders: List[FolderResponse]
