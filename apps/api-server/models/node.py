"""
Pydantic model for a registered storage node as tracked in the 'nodes' collection.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from core.types import PyObjectId
from core.enums import NodeStatus
from utils.time import current_time


class StorageNodeModel(BaseModel):
    """
    Represents one storage node registered with the API server.

    last_heartbeat is updated every time the node sends a heartbeat. The
    node monitor marks a node OFFLINE if this timestamp is more than 2
    minutes old, then triggers repair for any files stored on that node.
    """
    id: PyObjectId = Field(None, alias='_id')
    ip: str = Field(...)
    port: int = Field(...)
    status: str = NodeStatus.ONLINE
    available_capacity: Optional[int] = None  # Free disk space in bytes, updated per heartbeat.
    last_heartbeat: datetime = Field(default_factory=current_time)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
