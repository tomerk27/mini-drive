from enum import Enum

class ItemType(str, Enum):
    FOLDER = "folder"
    FILE = "file"

class ItemStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"