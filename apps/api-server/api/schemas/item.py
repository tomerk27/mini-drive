from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from core.enums import ItemType, SharePermission


class SharedUserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    permission: SharePermission


class ItemResponse(BaseModel):
    id: str
    name: str
    parent_id: Optional[str]
    item_type: ItemType
    created_at: datetime
    owner_id: str
    is_owner: bool = False
    starred_by: List[str] = []
    shared_with: List[SharedUserResponse] = []


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
    item_type: ItemType = ItemType.FOLDER


class ItemRename(BaseModel):
    new_name: str


class BreadcrumbItem(BaseModel):
    id: str
    name: str


class FolderContentResponse(BaseModel):
    folder: FolderResponse
    children: List[ItemResponse]
    breadcrumb: List[BreadcrumbItem] = []
