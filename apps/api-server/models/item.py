"""
Pydantic models for files and folders stored in the 'items' MongoDB collection.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from core.enums import ItemType, ItemStatus, SharePermission
from core.types import PyObjectId
from utils.time import current_time


class SharedUser(BaseModel):
    """A user that an item has been explicitly shared with, along with their permission level."""
    permission: SharePermission
    id: str
    email: Optional[str] = None


class ItemModel(BaseModel):
    """
    Base model for any item (file or folder) in the drive.

    Both FileModel and FolderModel extend this. shared_with stores all
    users the owner has explicitly granted access to. starred_by holds
    the IDs of users who have starred this item.
    """
    id: PyObjectId = Field(None, alias='_id')
    owner_id: str = Field(...)
    name: str
    item_type: ItemType
    parent_id: Optional[str] = Field(None)  # None only for the root folder.
    created_at: datetime = Field(default_factory=current_time)
    shared_with: List[SharedUser] = []
    starred_by: List[str] = []  # List of user IDs who starred this item.

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ChunkInfo(BaseModel):
    """
    Metadata for one chunk of a large file.

    Files are split into CHUNK_SIZE_BYTES pieces before upload. Each chunk
    is stored independently across up to 3 storage nodes for replication.

    chunk_hash is a SHA-256 hex digest used to verify data integrity on download.
    physical_name is the filename used on the storage node (UUID-based, not the original name).
    """
    chunk_index: int
    size: int
    chunk_hash: str
    physical_name: str
    node_ids: List[str] = []  # IDs of the storage nodes holding this chunk (up to 3).


class FileModel(ItemModel):
    """
    Extends ItemModel with file-specific fields and chunk metadata.

    status starts as PENDING while chunks are being uploaded and becomes
    COMPLETED once all chunks have been successfully stored.
    file_hash is a combined SHA-256 of all chunk hashes for end-to-end integrity.
    """
    item_type: ItemType = ItemType.FILE
    file_type: Optional[str] = None   # MIME type detected from the file header.
    size: Optional[int] = None        # Total file size in bytes.
    file_hash: Optional[str] = None   # SHA-256 hash computed from all chunk hashes.
    chunks: List[ChunkInfo] = []
    status: ItemStatus = ItemStatus.PENDING


class FolderModel(ItemModel):
    """A folder item. Folders have no file-specific fields — children are fetched by parent_id."""
    item_type: ItemType = ItemType.FOLDER
