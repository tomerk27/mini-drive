from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from web_api.routes import auth, items, user
from common import AppException, handle_exception, validation_error_handler

app = FastAPI()

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
