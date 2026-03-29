import os
import sys
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

# Add project root and libs to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "libs"))

from api.routes import auth, items, user
from core.exceptions import AppException, handle_exception, validation_error_handler
from infrastructure.storage.tracker.tracker_server import TrackerServer
from infrastructure.storage.tracker.data_server import DataServer
from infrastructure.storage.services.tracker_service import TrackerService

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Initialize servers
    tracker = TrackerServer()
    data_server = DataServer()

    # Start servers as background tasks
    asyncio.create_task(tracker.start())
    asyncio.create_task(data_server.start())

    # Start Maintenance Loop
    async def maintenance_task():
        print("[*] Maintenance Loop Started: Monitoring node health...")
        while True:
            try:
                await TrackerService.check_dead_nodes()
            except Exception as e:
                print(f"[!] Maintenance Error: {e}")
            await asyncio.sleep(60)
    
    asyncio.create_task(maintenance_task())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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
