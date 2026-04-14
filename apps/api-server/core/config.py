from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Taken from the .env file
    MONGO_URI: str
    SECRET_KEY: str
    STORAGE_ENCRYPTION_KEY: str
    

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_SCHEME: str = "Bearer"
    TOKEN_TYPE: str = "bearer"

    # Directory for temporary file storage (before forwarding to storage node)
    FILES_DIR: str = "settings/files"

    # Storage Server Configuration
    STORAGE_SERVER_HOST: str = "127.0.0.1"
    STORAGE_SERVER_PORT: int = 9000

    # File chunking
    CHUNK_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

    # Per-user storage quota
    MAX_STORAGE_BYTES: int = 5 * 1024 ** 3  # 5 GB
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()