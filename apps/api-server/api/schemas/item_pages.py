"""
Response schema for endpoints that return a flat list of items (starred, shared).
"""

from api.schemas.item import FileResponse, FolderResponse
from pydantic import BaseModel
from typing import List, Union


class ItemPageResponse(BaseModel):
    """A paginated-style wrapper around a list of file and folder responses."""
    items: List[Union[FileResponse, FolderResponse]]