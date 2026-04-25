from fastapi import APIRouter, status, Depends, File, UploadFile, Path, Response
from services.items_service import init_item, complete_item_upload, get_folder_service, remove_item_service, rename_item_service, get_file_preview_service, mark_item_as_starred_service, search_items_service
from services.share_service import share_item_service
from api.schemas.item import ItemResponse, FolderContentResponse, ItemRename, FolderCreate, ItemCreate
from api.schemas.share import ShareRequest
from models.user import User
from api.dependencies import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])


@router.post(
    "/upload/init", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
def upload_file(
    item_data: ItemCreate, current_user: User = Depends(get_current_user)
) -> ItemResponse:
    return init_item(item_data, current_user.id)


@router.post(
    "/upload/folder", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
def upload_folder(
    folder_data: FolderCreate, current_user: User = Depends(get_current_user)
):
    return init_item(folder_data, current_user.id)


@router.post(
    "/upload/{item_id}/content",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
)
def upload_content(
    item_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> ItemResponse:
    return complete_item_upload(item_id, current_user.id, file, current_user.id)


@router.get(
    "/get/{folder_id}",
    response_model=FolderContentResponse,
    status_code=status.HTTP_200_OK,
)
def get_folder(
    folder_id: str = Path(...), current_user: User = Depends(get_current_user)
) -> ItemResponse:
    return get_folder_service(folder_id, current_user.id)


@router.get('/search', status_code=status.HTTP_200_OK)
def search_items(
    query: str,
    current_user: User = Depends(get_current_user)
):
    return search_items_service(query, current_user.id)


@router.delete("/remove/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: str, current_user: User = Depends(get_current_user)):
    remove_item_service(item_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/rename/{item_id}", status_code=status.HTTP_200_OK)
def rename_item(
    item_id: str,
    rename_schema: ItemRename,
    current_user: User = Depends(get_current_user),
):
    rename_item_service(item_id, current_user.id, rename_schema.new_name)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/preview/{item_id}", status_code=status.HTTP_200_OK)
def get_file_preview(
    item_id: str, current_user: User = Depends(get_current_user)
):
    return get_file_preview_service(item_id, current_user.id)


@router.patch("/markAsStarred/{item_id}", status_code=status.HTTP_200_OK)
def mark_item_as_starred(
    item_id: str, current_user: User = Depends(get_current_user)
):
    mark_item_as_starred_service(item_id, current_user.id)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/{item_id}/share", status_code=status.HTTP_200_OK)
def share_item(
    item_id: str,
    share_schema: ShareRequest,
    current_user: User = Depends(get_current_user),
):
    share_item_service(share_schema, item_id, current_user.id)
    return Response(status_code=status.HTTP_200_OK)
