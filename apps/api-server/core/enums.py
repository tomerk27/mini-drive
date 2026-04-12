from enum import Enum


class ItemType(str, Enum):
    FOLDER = "folder"
    FILE = "file"


class ItemStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class SharePermission(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"


class NodeStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
