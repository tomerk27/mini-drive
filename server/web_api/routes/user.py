from fastapi import APIRouter, status, Depends
from common.models.user import User
from web_api.dependencies import get_current_user
from web_api.services.user_service import get_starred_items_service, get_shared_items_service
from web_api.schemas.item_pages import ItemPageResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/starred-items', status_code=status.HTTP_200_OK, response_model=ItemPageResponse)
async def get_starred_items(
    current_user: User = Depends(get_current_user)
):
    starred_items = await get_starred_items_service(current_user.id)

    return starred_items

@router.get('/shared-with-me', status_code=status.HTTP_200_OK, response_model=ItemPageResponse)
async def get_shared_with_me_items(
    current_user: User = Depends(get_current_user)
):
    shared_items = await get_shared_items_service(current_user.id)

    return shared_items