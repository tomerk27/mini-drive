from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Taken from the .env file
    mongo_uri: str
    secret_key: str

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    auth_scheme: str = "Bearer"
    token_type: str = "bearer"

    class Config:
        env_file=".env"

settings = Settings()