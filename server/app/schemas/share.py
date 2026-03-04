from pydantic import BaseModel, EmailStr
from app.utils.item_utils import SharePermission

class ShareRequest(BaseModel):
    permission: SharePermission
    email: EmailStr