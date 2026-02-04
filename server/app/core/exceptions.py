from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings

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
            headers={"WWW-Authenticate": settings.auth_scheme}
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
        super.__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
class ResourceNotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super.__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

async def handle_exception(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "Invalid email or password"}
    )