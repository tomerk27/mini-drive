from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    # Taken from the .env file
    MONGO_URI: str
    SECRET_KEY: str
    STORAGE_ENCRYPTION_KEY: str
    

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_SCHEME: str = "Bearer"
    TOKEN_TYPE: str = "bearer"

    # Storage Server Configuration
    STORAGE_SERVER_HOST: str = "127.0.0.1"
    STORAGE_SERVER_PORT: int = 9000

    # File chunking
    CHUNK_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

    # Per-user storage quota
    MAX_STORAGE_BYTES: int = 5 * 1024 ** 3  # 5 GB
    MAX_FILE_SIZE_BYTES: int = 500 * 1024 * 1024  # 500 MB
    
    BLOCKED_EXTENSIONS: ClassVar[set] = {'.jar', '.sh', '.ps1', '.cmd', '.exe', '.msi', '.scr', '.vbs', '.dll', '.bat'}

    BLOCKED_MIME_TYPES = {                                                                                                                                                             
      "application/x-executable",    # Linux ELF binaries
      "application/x-dosexec",       # Windows PE (.exe, .dll)                                                                                                                       
      "application/x-sharedlib",     # .so shared libraries                                                                                                                          
      "application/x-msi",           # Windows installer   
  }       

    class Config:
        env_file = (".env", ".env.local")
        case_sensitive = False

settings = Settings()