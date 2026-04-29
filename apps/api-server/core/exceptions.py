"""
Custom exception classes and FastAPI error handlers for CyberDrive.

All domain errors extend AppException, which carries an HTTP status code
and a user-facing detail message. The two handler functions at the bottom
convert these into clean JSON responses.
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from core.config import settings


class AppException(Exception):
    """
    Base class for all application-level HTTP errors.

    Args:
        status_code: The HTTP status code to return (e.g. 404, 403).
        detail: Human-readable message sent back to the client.
        headers: Optional extra response headers (used for WWW-Authenticate).
    """
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class UserNotFoundError(AppException):
    """Raised when login credentials don't match any user. Returns 401."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
            headers={"WWW-Authenticate": settings.AUTH_SCHEME}
        )


class ExistingUserError(AppException):
    """Raised when someone tries to register with an email already in use. Returns 409."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already in use"
        )


class ExistingItemError(AppException):
    """Raised when a file or folder with the same name already exists in the same location. Returns 409."""
    def __init__(self, filename):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A file named '{filename}' already exists in this destination."
        )


class TokenCredentialsError(AppException):
    """Raised when a JWT token is missing, expired, or invalid. Returns 401."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": settings.AUTH_SCHEME}
        )


class ResourceNotFoundError(AppException):
    """Raised when an item, user, or any other resource doesn't exist in the DB. Returns 404."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class PermissionError(AppException):
    """Raised when a user tries to perform an action they don't have permission for. Returns 403."""
    def __init__(self, action: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have a premission to {action} this content"
        )


class DataBaseError(AppException):
    """Raised when a MongoDB write or update operation fails unexpectedly. Returns 500."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data base error"
        )


class StorageServerError(AppException):
    """Raised when communication with a storage node fails or a node is unavailable. Returns 500."""
    def __init__(self, detail="Storage server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ItemIsFolderError(AppException):
    """Raised when a file-only operation (like download) is called on a folder. Returns 400."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot perform this action: the requested item is a folder, not a file."
        )


class StorageLimitExceededError(AppException):
    """Raised when an upload would push the user past their 5 GB quota. Returns 507."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
            detail="Storage limit exceeded. You have used your 5 GB quota."
        )


class FileTypeNotAllowedError(AppException):
    """Raised when the uploaded file extension or MIME type is on the blocked list. Returns 415."""
    def __init__(self, ext: str):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{ext}' is not allowed"
        )


class SelfShareError(AppException):
    """Raised when a user tries to share an item with themselves. Returns 400."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot share an item with yourself."
        )


async def handle_exception(request: Request, exc: AppException):
    """FastAPI handler: converts any AppException into a JSON error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    FastAPI handler: converts Pydantic validation errors into a friendly message.

    Returns a plain "Invalid input" for most errors, but provides a more
    specific message for known fields like 'username'.
    """
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