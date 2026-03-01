from app.schemas.item import FileResponse, FolderResponse
from pydantic import BaseModel
from typing import List, Union

class StarredItemsResponse(BaseModel):
    starred_items: List[Union[FileResponse, FolderResponse]]