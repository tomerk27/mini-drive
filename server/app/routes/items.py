from fastapi import APIRouter, status, Depends, File, UploadFile
from app.services.items_service import init_item, complete_item_upload
from app.schemas.item import ItemResponse, FileCreate
from app.models.user import User
from app.dependencies import get_current_user
from app.utils.mappers import map_item_to_response

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.post("/upload/init", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    item_data: FileCreate,
    current_user: User = Depends(get_current_user)
) -> ItemResponse:
    new_item = await init_item(item_data, current_user.id)
    return map_item_to_response(new_item, current_user)

@router.post("/upload/{item_id}/content", response_model=ItemResponse)
async def upload_content(
    item_id: str, 
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> ItemResponse:
    completed_item = await complete_item_upload(
        item_id=item_data.id,
        owner_id=current_user.id,
        file=file
    )

    return map_item_to_response(complete_item, current_user)