from pydantic import BaseModel, EmailStr
from common import SharePermission

class ShareRequest(BaseModel):
    permission: SharePermission
    email: EmailStr