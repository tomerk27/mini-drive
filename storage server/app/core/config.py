import os
from dotenv import load_dotenv

# Path to the 'storage server' directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(DOTENV_PATH)

class Settings:
    def __init__(self):
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", 9000))
        self.STORAGE_ENCRYPTION_KEY = os.getenv("STORAGE_ENCRYPTION_KEY")
        self.STORAGE_DIR = os.path.join(BASE_DIR, "data")

settings = Settings()
