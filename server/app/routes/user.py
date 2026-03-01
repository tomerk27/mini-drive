from fastapi import APIRouter, status, Depends
from app.models.user import User
from app.dependencies import get_current_user
from app.services.user_service import get_starred_items_service
from app.schemas.starred_items import StarredItemsResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/starredItems', status_code=status.HTTP_200_OK, response_model=StarredItemsResponse)
async def get_starred_items(
    current_user: User = Depends(get_current_user)
):
    starred_items = await get_starred_items_service(current_user.id)

    return starred_items