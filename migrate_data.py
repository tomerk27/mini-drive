import asyncio
import os
import hashlib
import shutil
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# #############################################################################
# CONFIGURATION
# #############################################################################
# Look for .env in the server folder
load_dotenv("server/.env")

# Check for both possible names
MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGO_URL")
OLD_FILES_DIR = "server/settings/files"
NEW_FILES_DIR = "storage server/data"

async def calculate_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()

async def migrate():
    print("[*] Starting Data Migration to Distributed Storage...")
    
    if not MONGO_URI:
        print("[!] Error: MONGO_URI not found in .env")
        return

    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database()
    items = db['items']
    
    # Ensure new storage directory exists
    os.makedirs(NEW_FILES_DIR, exist_ok=True)

    # 1. Find all items that have 'physical_path' (the old field)
    cursor = items.find({"physical_path": {"$exists": True}})
    migrated_count = 0

    async for item in cursor:
        old_path = item.get("physical_path")
        item_id = item.get("_id")
        
        # Determine the physical filename from the old path
        filename = os.path.basename(old_path)
        source_path = os.path.join(OLD_FILES_DIR, filename)
        target_path = os.path.join(NEW_FILES_DIR, filename)

        print(f"[*] Migrating item {item.get('name')} (ID: {item_id})...")

        # 2. Check if the physical file exists in the old location
        if os.path.exists(source_path):
            try:
                # Calculate the hash for integrity
                file_hash = await calculate_hash(source_path)
                file_size = os.path.getsize(source_path)

                # Move the file to the new storage node's data folder
                shutil.move(source_path, target_path)
                print(f"    [+] Moved physical file to storage node.")

                # 3. Update the Database record
                await items.update_one(
                    {"_id": item_id},
                    {
                        "$set": {
                            "physical_name": filename,
                            "file_hash": file_hash,
                            "size": file_size,
                            "status": "completed"
                        },
                        "$unset": {"physical_path": ""} # Remove the old field
                    }
                )
                print(f"    [+] Database record updated and 'physical_path' removed.")
                migrated_count += 1

            except Exception as e:
                print(f"    [!] Error migrating file {filename}: {e}")
        else:
            print(f"    [!] Warning: Physical file {filename} not found in {OLD_FILES_DIR}. Skipping.")

    print(f"\n[OK] Migration finished! {migrated_count} items successfully migrated.")
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate())
