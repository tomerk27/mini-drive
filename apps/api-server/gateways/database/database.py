"""
MongoDB connection setup for the API server.

Creates a single synchronous PyMongo client shared across the process.
The database name is taken from the connection string itself (get_default_database),
so the MONGO_URI must include the database name (e.g. .../cyberdrive).
"""

from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("No MONGO_URI found in .env file")

# Module-level client — reused for every request (connection pooling handled by PyMongo).
client = pymongo.MongoClient(MONGO_URI)

# The database name is inferred from the URI path (e.g. /cyberdrive).
db = client.get_default_database()


def get_collection(collection_name: str):
    """
    Returns a PyMongo Collection object for the given collection name.

    Args:
        collection_name: e.g. "users", "items", "nodes".

    Returns:
        A pymongo.collection.Collection ready for queries.
    """
    return db[collection_name]
