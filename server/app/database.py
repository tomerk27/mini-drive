from dotenv import load_dotenv
import motor.motor_asyncio
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URL: 
    raise ValueError("No MONGO_URL found in .env file")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = client[DB_NAME]

def get_user_collection():
    return db["users"]