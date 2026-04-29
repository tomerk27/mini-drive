"""
Configuration for the storage node, loaded from its local .env file.

If NODE_ID is not set in .env, a random short ID is generated and written
back to .env so the node keeps the same identity across restarts.
"""

import os
import uuid
from dotenv import load_dotenv

# Resolve paths relative to the storage-node directory, not the cwd.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
DOTENV_LOCAL_PATH = os.path.join(BASE_DIR, ".env.local")

# Load base config, then let .env.local override it in non-production environments.
load_dotenv(DOTENV_PATH)
if os.getenv("NODE_ENV") != "production":
    load_dotenv(DOTENV_LOCAL_PATH, override=True)


class Settings:
    """
    Runtime settings for the storage node.

    Fields:
        NODE_ID: Unique string identifier. Auto-generated and persisted to .env
            if not already set, so the node keeps the same ID after restarts.
        HOST: Local IP this node binds to (usually 127.0.0.1).
        PORT: Port the node listens on for file commands (unique per node).
        TRACKER_HOST: IP of the API server to send heartbeats to.
        TRACKER_PORT: Port the HeartbeatServer is listening on (default 9001).
        STORAGE_ENCRYPTION_KEY: Fernet key — must match the API server's key exactly.
        STORAGE_DIR: Local directory where uploaded files are written.
    """

    def __init__(self):
        self.NODE_ID = os.getenv("NODE_ID")
        if not self.NODE_ID:
            # Generate a short random ID and persist it so it survives restarts.
            self.NODE_ID = f"Node-{str(uuid.uuid4())[:4]}"
            with open(DOTENV_PATH, 'a') as f:
                f.write(f"\nNODE_ID={self.NODE_ID}")

        self.HOST = os.getenv("HOST")                           # Local listener IP
        self.PORT = int(os.getenv("PORT"))                      # Local listener port
        self.TRACKER_HOST = os.getenv("TRACKER_HOST")          # API server IP
        self.TRACKER_PORT = int(os.getenv("TRACKER_PORT"))     # HeartbeatServer port
        self.STORAGE_ENCRYPTION_KEY = os.getenv("STORAGE_ENCRYPTION_KEY")
        self.STORAGE_DIR = os.path.join(BASE_DIR, "data")      # Files stored here


settings = Settings()
