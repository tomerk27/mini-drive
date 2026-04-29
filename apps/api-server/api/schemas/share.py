"""
Request schema for the share endpoint.
"""

from pydantic import BaseModel, EmailStr
from core.enums import SharePermission


class ShareRequest(BaseModel):
    """Request body for POST /items/{item_id}/share."""
    permission: SharePermission  # VIEWER or EDITOR (owners cannot be added via share).
    email: EmailStr              # Email of the user to share with.
