from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from core.types import PyObjectId
from core.enums import NodeStatus
from utils.time import current_time


class StorageNodeModel(BaseModel):
    id: PyObjectId = Field(None, alias='_id')
    ip: str = Field(...)
    port: int = Field(...)
    status: str = NodeStatus.ONLINE
    available_capacity: Optional[int] = None  # bytes
    last_heartbeat: datetime = Field(default_factory=current_time)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
