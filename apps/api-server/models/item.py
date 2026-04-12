from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from core.enums import ItemType, ItemStatus, SharePermission
from core.types import PyObjectId
from utils.time import current_time


class SharedUser(BaseModel):
    permission: SharePermission
    id: str
    email: Optional[str] = None


class ItemModel(BaseModel):
    id: PyObjectId = Field(None, alias='_id')

    owner_id: str = Field(...)
    name: str
    item_type: ItemType

    parent_id: Optional[str] = Field(None)

    created_at: datetime = Field(default_factory=current_time)

    shared_with: List[SharedUser] = []
    starred_by: List[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ChunkInfo(BaseModel):
    chunk_index: int
    size: int
    chunk_hash: str
    physical_name: str
    node_ids: List[str] = []


class FileModel(ItemModel):
    item_type: ItemType = ItemType.FILE

    file_type: Optional[str] = None
    size: Optional[int] = None
    file_hash: Optional[str] = None

    chunks: List[ChunkInfo] = []

    status: ItemStatus = ItemStatus.PENDING


class FolderModel(ItemModel):
    item_type: ItemType = ItemType.FOLDER
