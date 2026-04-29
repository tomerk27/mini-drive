"""
CyberDrive API Server entry point.

Starts FastAPI and launches three background daemon threads:
  - HeartbeatServer (port 9001): receives periodic heartbeats from storage nodes.
  - DataServer (port 9000): keeps persistent connections open for UPLOAD/DOWNLOAD/DELETE.
  - NodeMonitor: checks every 60 s for dead nodes and triggers self-healing repair.
"""

import os
import sys
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

# Add project root and shared libs to Python path so imports work from any cwd.
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "libs"))

from api.routes import auth, items, user
from core.exceptions import AppException, handle_exception, validation_error_handler
from gateways.storage.servers.heartbeat_server import HeartbeatServer
from gateways.storage.servers.data_server import DataServer
from workers.node_monitor import run_node_monitor

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """Launches background infrastructure threads when the API server starts up."""
    threading.Thread(target=HeartbeatServer().start, daemon=True).start()
    threading.Thread(target=DataServer().start, daemon=True).start()
    threading.Thread(target=run_node_monitor, daemon=True).start()


# Allow the web client (dev and prod) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cyberdrive24.com", "http://localhost:5173", "http://192.168.1.200:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global error handlers so all AppExceptions return clean JSON responses.
app.add_exception_handler(AppException, handle_exception)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(auth.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.get("/")
def read_root():
    """Health-check endpoint — confirms the server is running."""
    return {"message": "Google Drive Clone Server is Running!", "status": "OK"}
