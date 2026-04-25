from fastapi import APIRouter, status, Depends
from models.user import User
from api.dependencies import get_current_user
from services.user_service import get_starred_items_service, get_shared_items_service, get_storage_service
from api.schemas.item_pages import ItemPageResponse
from api.schemas.user import StorageResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/starred-items', status_code=status.HTTP_200_OK, response_model=ItemPageResponse)
def get_starred_items(
    current_user: User = Depends(get_current_user)
):
    return get_starred_items_service(current_user.id)


@router.get('/shared-with-me', status_code=status.HTTP_200_OK, response_model=ItemPageResponse)
def get_shared_with_me_items(
    current_user: User = Depends(get_current_user)
):
    return get_shared_items_service(current_user.id)


@router.get('/storage', status_code=status.HTTP_200_OK, response_model=StorageResponse)
def get_storage(current_user: User = Depends(get_current_user)):
    return get_storage_service(current_user.id)
