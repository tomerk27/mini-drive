import os
import sys
import asyncio
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
async def startup_event():
    asyncio.create_task(HeartbeatServer().start())
    asyncio.create_task(DataServer().start())
    asyncio.create_task(run_node_monitor())


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cyberdrive24.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, handle_exception)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Google Drive Clone Server is Running!", "status": "OK"}
