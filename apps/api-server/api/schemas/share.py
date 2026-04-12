from pydantic import BaseModel, EmailStr
from core.enums import SharePermission


class ShareRequest(BaseModel):
    permission: SharePermission
    email: EmailStr
