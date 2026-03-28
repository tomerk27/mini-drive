from pydantic import BaseModel, EmailStr
from common.utils.item_utils import SharePermission

class ShareRequest(BaseModel):
    permission: SharePermission
    email: EmailStr