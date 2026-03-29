from pydantic import BaseModel, EmailStr
from utils.item_utils import SharePermission

class ShareRequest(BaseModel):
    permission: SharePermission
    email: EmailStr