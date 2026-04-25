from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("No MONGO_URI found in .env file")

client = pymongo.MongoClient(MONGO_URI)

db = client.get_default_database()


def get_collection(collection_name):
    return db[collection_name]
