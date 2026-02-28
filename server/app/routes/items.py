from fastapi import APIRouter, status, Depends, File, UploadFile, Path, Response
from app.services.items_service import init_item, complete_item_upload, get_folder_service, remove_item_service, rename_item_service, get_file_preview_service
from app.schemas.item import ItemResponse, FileCreate, FolderContentResponse, ItemRename, FolderCreate
from app.models.user import User
from app.dependencies import get_current_user

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
    return new_item

@router.post("/upload/folder", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def upload_folder(
    folder_data: FolderCreate,
    current_user: User = Depends(get_current_user)
):
    new_item = await init_item(folder_data, current_user.id)

    return new_item

@router.post("/upload/{item_id}/content", response_model=ItemResponse,status_code=status.HTTP_200_OK)
async def upload_content(
    item_id: str, 
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> ItemResponse:
    completed_item = await complete_item_upload(item_id, current_user.id, file, current_user.id)

    return completed_item

@router.get('/get/{folder_id}', response_model=FolderContentResponse, status_code=status.HTTP_200_OK)
async def get_folder(
    folder_id: str = Path(...), 
    current_user: User = Depends(get_current_user)
    ) -> ItemResponse:
    folder = await get_folder_service(folder_id, current_user.id)

    return folder

@router.delete("/remove/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(
    item_id: str,
    current_user: User = Depends(get_current_user)
):
    await remove_item_service(item_id, current_user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/rename/{item_id}", status_code=status.HTTP_200_OK)
async def rename_item(
    item_id: str,
    rename_schema: ItemRename,
    current_user: User = Depends(get_current_user)
):
    await rename_item_service(item_id, current_user.id, rename_schema.new_name)

    return Response(status_code=status.HTTP_200_OK)

@router.get('/preview/{item_id}')
async def get_file_preview(
    item_id: str,
    current_user: User = Depends(get_current_user)
):
    file_preview = await get_file_preview_service(item_id, current_user.id)

    return file_preview