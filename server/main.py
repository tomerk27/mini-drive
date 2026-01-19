from fastapi import FastAPI

app = FastAPI()

# בדיקה שהשרת עובד
@app.get("/")
def read_root():
    return {"message": "Google Drive Clone Server is Running!", "status": "OK"}

# דוגמה לנתיב נוסף
@app.get("/test")
def test_route():
    return {"data": "This is a test route"}