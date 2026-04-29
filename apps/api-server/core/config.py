"""
Application-wide settings loaded from .env / .env.local.

Pydantic-settings reads each field from the matching environment variable.
Required fields (MONGO_URI, SECRET_KEY, STORAGE_ENCRYPTION_KEY) must be
present in .env or the server will refuse to start.
"""

from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    # --- Required: must be set in .env ----------------------------------------

    # MongoDB Atlas connection string (e.g. mongodb+srv://user:pass@cluster/dbname).
    MONGO_URI: str

    # Secret used to sign JWT tokens. Use a long, random string — changing this
    # invalidates all existing sessions.
    SECRET_KEY: str

    # Fernet key for encrypting data between the API server and storage nodes.
    # Must be identical on every storage node's .env.
    STORAGE_ENCRYPTION_KEY: str

    # --- JWT settings ----------------------------------------------------------

    # Signing algorithm for JWTs (HS256 = HMAC-SHA256).
    ALGORITHM: str = "HS256"

    # Minutes before a JWT access token expires and the user must log in again.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    AUTH_SCHEME: str = "Bearer"
    TOKEN_TYPE: str = "bearer"

    # --- Storage node network --------------------------------------------------

    # Host and port the DataServer listens on for persistent storage-node connections.
    STORAGE_SERVER_HOST: str = "127.0.0.1"
    STORAGE_SERVER_PORT: int = 9000

    # --- File chunking ---------------------------------------------------------

    # Large files are split into chunks before being sent to storage nodes.
    # Each chunk is replicated independently across 3 nodes.
    CHUNK_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB per chunk

    # --- Per-user quotas -------------------------------------------------------

    MAX_STORAGE_BYTES: int = 5 * 1024 ** 3    # 5 GB total per user
    MAX_FILE_SIZE_BYTES: int = 3 * 1024 ** 3  # single file cap (also bounded by quota)

    # --- Security: blocked file types -----------------------------------------

    # File extensions the server will always reject, regardless of MIME type.
    BLOCKED_EXTENSIONS: ClassVar[set] = {'.jar', '.sh', '.ps1', '.cmd', '.exe', '.msi', '.scr', '.vbs', '.dll', '.bat'}

    # MIME types detected from the file's binary header that are also blocked.
    BLOCKED_MIME_TYPES: ClassVar[set] = {
        "application/x-executable",    # Linux ELF binaries
        "application/x-dosexec",       # Windows PE (.exe, .dll)
        "application/x-sharedlib",     # .so shared libraries
        "application/x-msi",           # Windows installer
    }

    class Config:
        env_file = (".env", ".env.local")
        case_sensitive = False


settings = Settings()