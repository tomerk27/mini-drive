import os
import uuid
from dotenv import load_dotenv

# Path to the 'storage server' directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
DOTENV_LOCAL_PATH = os.path.join(BASE_DIR, ".env.local")

load_dotenv(DOTENV_PATH)
if os.getenv("NODE_ENV") != "production":
    load_dotenv(DOTENV_LOCAL_PATH, override=True)

class Settings:
    def __init__(self):
        self.NODE_ID = os.getenv("NODE_ID")
        if not self.NODE_ID:
            self.NODE_ID = f"Node-{str(uuid.uuid4())[:4]}"
            with open(DOTENV_PATH, 'a') as f:
                f.write(f"\nNODE_ID={self.NODE_ID}")

        self.HOST = os.getenv("HOST") # Local listener IP
        self.PORT = int(os.getenv("PORT")) # Local listener Port (for uploads)

        self.TRACKER_HOST = os.getenv("TRACKER_HOST") # Main Server IP
        self.TRACKER_PORT = int(os.getenv("TRACKER_PORT"))    # Main Server Port

        self.STORAGE_ENCRYPTION_KEY = os.getenv("STORAGE_ENCRYPTION_KEY")
        self.STORAGE_DIR = os.path.join(BASE_DIR, "data")

settings = Settings()
