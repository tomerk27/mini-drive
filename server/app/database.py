from dotenv import load_dotenv
import motor.motor_asyncio
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI: 
    raise ValueError("No MONGO_URL found in .env file")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db = client.get_default_database()

def get_users_collection():
    return db["users"]