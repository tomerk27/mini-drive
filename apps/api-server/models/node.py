from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from utils.db_utils import PyObjectId
from utils.time import current_time
from utils.node_utils import NodeStatus

class StorageNodeModel(BaseModel):
    id: PyObjectId = Field(None, alias='_id')
    ip: str = Field(...)
    port: int = Field(...)
    status: str = NodeStatus.ONLINE  # "online" or "offline"
    available_capacity: Optional[int] = None  # in bytes
    last_heartbeat: datetime = Field(default_factory=current_time)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True