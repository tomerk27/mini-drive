from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from web_api.routes import auth, items, user
from common import AppException, handle_exception, validation_error_handler
from storage_engine.tracker.tracker_server import TrackerServer
from storage_engine.tracker.data_server import DataServer
import threading
import asyncio
from storage_engine import TrackerService

app = FastAPI()

# Start the Tracker Server in a background thread
def start_tracker():
    tracker = TrackerServer()
    tracker.start()

# Start the Data Server in a background thread (Reversed roles: Listener)
def start_data_server():
    data_server = DataServer()
    data_server.start()

def start_maintenance_loop():
    """Periodic health check for dead nodes (Runs every 60s)."""
    async def maintenance_task():
        print("[*] Maintenance Loop Started: Monitoring node health...")
        while True:
            try:
                await TrackerService.check_dead_nodes()
            except Exception as e:
                print(f"[!] Maintenance Error: {e}")
            await asyncio.sleep(60)

    # Initialize a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(maintenance_task())

threading.Thread(target=start_tracker, daemon=True).start()
threading.Thread(target=start_data_server, daemon=True).start()
threading.Thread(target=start_maintenance_loop, daemon=True).start()

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
