import os
import uuid
from dotenv import load_dotenv

# Path to the 'storage server' directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(DOTENV_PATH)

class Settings:
    def __init__(self):
        self.NODE_ID = os.getenv("NODE_ID")
        if not self.NODE_ID:
            self.NODE_ID = f"Node-{str(uuid.uuid4())[:4]}"
            with open(DOTENV_PATH, 'a') as f:
                f.write(f"\nNODE_ID={self.NODE_ID}")
        
        self.HOST = os.getenv("HOST")
        self.PORT = int(os.getenv("PORT"))
        self.STORAGE_ENCRYPTION_KEY = os.getenv("STORAGE_ENCRYPTION_KEY")
        self.STORAGE_DIR = os.path.join(BASE_DIR, "data")

settings = Settings()
