"""
Request/response schemas for item (file and folder) endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime
from core.enums import ItemType, SharePermission


class SharedUserResponse(BaseModel):
    """A user the item is shared with, included in responses only for the owner."""
    id: str
    email: Optional[str] = None
    permission: SharePermission


class ItemResponse(BaseModel):
    """Base public representation of any item. Returned by most item endpoints."""
    id: str
    name: str
    parent_id: Optional[str]
    item_type: ItemType
    created_at: datetime
    owner_id: str
    owner_username: Optional[str] = None   # Populated when viewing items shared by others.
    is_owner: bool = False                  # True if the requesting user owns this item.
    starred_by: List[str] = []
    shared_with: List[SharedUserResponse] = []  # Only populated for the item owner.


class FileResponse(ItemResponse):
    """Extends ItemResponse with file-specific fields (MIME type and size)."""
    item_type: ItemType = ItemType.FILE
    file_type: Optional[str] = None
    size: Optional[int] = None


class FolderResponse(ItemResponse):
    """Folder variant of ItemResponse (no extra fields — children fetched separately)."""
    item_type: ItemType = ItemType.FOLDER


class ItemCreate(BaseModel):
    """Request body for POST /items/upload/init (file or folder)."""
    name: str
    parent_id: Optional[str] = None
    item_type: ItemType


class FolderCreate(BaseModel):
    """Request body for POST /items/upload/folder."""
    name: str
    parent_id: Optional[str] = None
    item_type: ItemType = ItemType.FOLDER


class ItemRename(BaseModel):
    """Request body for PATCH /items/rename/{item_id}."""
    new_name: str


class BreadcrumbItem(BaseModel):
    """One step in the folder navigation trail (id + display name)."""
    id: str
    name: str


class FolderContentResponse(BaseModel):
    """Returned by GET /items/get/{folder_id} — folder metadata, its children, and breadcrumb path."""
    folder: FolderResponse
    children: List[Union[FileResponse, FolderResponse]]
    breadcrumb: List[BreadcrumbItem] = []
