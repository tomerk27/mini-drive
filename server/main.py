import os
import sys
import threading
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

# Add the project root (parent directory) to sys.path so 'shared' can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_api.routes import auth, items, user
from common.core.exceptions import AppException, handle_exception, validation_error_handler
from storage_engine.tracker.tracker_server import TrackerServer
from storage_engine.tracker.data_server import DataServer
from storage_engine.services.tracker_service import TrackerService

app = FastAPI()

# 1. Global event loop reference
main_loop = None

@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()
    
    # Start the Tracker Server in a background thread, passing the main loop
    def start_tracker():
        tracker = TrackerServer(main_loop)
        tracker.start()

    # Start the Data Server in a background thread
    def start_data_server():
        data_server = DataServer()
        data_server.start()

    # Start the Maintenance Loop in a background thread
    def start_maintenance_loop():
        async def maintenance_task():
            print("[*] Maintenance Loop Started: Monitoring node health...")
            while True:
                try:
                    await TrackerService.check_dead_nodes()
                except Exception as e:
                    print(f"[!] Maintenance Error: {e}")
                await asyncio.sleep(60)
        
        # Run the task in the captured main loop
        asyncio.run_coroutine_threadsafe(maintenance_task(), main_loop)

    threading.Thread(target=start_tracker, daemon=True).start()
    threading.Thread(target=start_data_server, daemon=True).start()
    start_maintenance_loop()

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
