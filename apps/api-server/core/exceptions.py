from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from core.config import settings

class AppException(Exception): 
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class UserNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
            headers={"WWW-Authenticate": settings.AUTH_SCHEME}
        )

class ExistingUserError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already in use"
        )

class ExistingItemError(AppException):
    def __init__(self, filename):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A file named '{filename}' already exists in this destination."        
        )

class TokenCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": settings.AUTH_SCHEME}
        )

        
class ResourceNotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class PermissionError(AppException): 
    def __init__(self, action: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have a premission to {action} this content"
        )

class DataBaseError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data base error"
        )

class StorageServerError(AppException):
    def __init__(self, detail = "Storage server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ItemIsFolderError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot perform this action: the requested item is a folder, not a file."
        )

class StorageLimitExceededError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
            detail="Storage limit exceeded. You have used your 5 GB quota."
        )

class FileTypeNotAllowedError(AppException):
    def __init__(self, ext: str):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{ext}' is not allowed"
        )

class SelfShareError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot share an item with yourself."
        )

async def handle_exception(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )
        
async def validation_error_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    field = error.get("loc", ["field"])[-1]
    error_type = error.get("type", "")

    if field == "username" and "min_length" in error_type:
        detail = "Username is too short"
    else:
        detail = "Invalid input"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": detail}
    )