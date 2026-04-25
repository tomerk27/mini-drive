import os
import sys
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

# Add project root and shared libs to Python path
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
    threading.Thread(target=HeartbeatServer().start, daemon=True).start()
    threading.Thread(target=DataServer().start, daemon=True).start()
    threading.Thread(target=run_node_monitor, daemon=True).start()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cyberdrive24.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, handle_exception)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(auth.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Google Drive Clone Server is Running!", "status": "OK"}
