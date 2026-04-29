"""
Application-wide string enums shared across models, services, and routes.
"""

from enum import Enum


class ItemType(str, Enum):
    """Whether a stored item is a file or a folder."""
    FOLDER = "folder"
    FILE = "file"


class ItemStatus(str, Enum):
    """
    Tracks whether a file upload is complete.

    PENDING: the file record exists in the DB but content has not been uploaded yet.
    COMPLETED: all chunks have been stored on the storage nodes successfully.
    """
    PENDING = "pending"
    COMPLETED = "completed"


class SharePermission(str, Enum):
    """
    Access levels for shared items.

    VIEWER: can read and preview only.
    EDITOR: can read, rename, delete, and share.
    OWNER: full control (same as EDITOR but used to identify the original creator).
    """
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"


class NodeStatus(str, Enum):
    """Health status of a storage node as tracked in the database."""
    ONLINE = "online"
    OFFLINE = "offline"
