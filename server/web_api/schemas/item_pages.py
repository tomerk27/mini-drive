from web_api import FileResponse, FolderResponse
from pydantic import BaseModel
from typing import List, Union

class ItemPageResponse(BaseModel):
    items: List[Union[FileResponse, FolderResponse]]