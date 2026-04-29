"""
migrate_data.py

One-time migration script used when the project moved from a single-server
architecture (where files lived at server/settings/files/) to the distributed
storage node architecture (where files live at storage server/data/).

What it does:
  1. Finds every MongoDB item document that still has the old `physical_path` field.
  2. Moves the actual file from the old directory to the new storage node data folder.
  3. Computes a SHA-256 hash and records the file size for integrity tracking.
  4. Updates the DB record with the new fields and removes `physical_path`.

Run once from the project root: python tools/migrate_data.py
"""

import asyncio
import os
import hashlib
import shutil
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Look for .env in the server folder (old layout)
load_dotenv("server/.env")

# Accept either MONGO_URI or MONGO_URL — the key name changed during refactoring
MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGO_URL")

# Physical file locations before and after the migration
OLD_FILES_DIR = "server/settings/files"
NEW_FILES_DIR = "storage server/data"


async def calculate_hash(file_path: str) -> str:
    """
    Computes the SHA-256 hash of a file for integrity verification.

    Reads the file in 4 KB chunks to avoid loading large files into memory.

    Args:
        file_path: Absolute or relative path to the file to hash.

    Returns:
        Lowercase hex string of the SHA-256 digest.
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


async def migrate():
    """
    Runs the full migration from the old single-server layout to distributed storage.

    Steps for each item:
      1. Locate the file using the old `physical_path` field.
      2. Hash and size the file, then move it to NEW_FILES_DIR.
      3. Update the MongoDB record with `physical_name`, `file_hash`, `size`,
         `status=completed`, and remove the stale `physical_path` field.

    Items whose physical file is missing on disk are skipped with a warning.
    """
    print("[*] Starting Data Migration to Distributed Storage...")

    if not MONGO_URI:
        print("[!] Error: MONGO_URI not found in .env")
        return

    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_default_database()
    items = db['items']

    # Create the target directory if it does not exist yet
    os.makedirs(NEW_FILES_DIR, exist_ok=True)

    # Query only items that still use the old single-server path field
    cursor = items.find({"physical_path": {"$exists": True}})
    migrated_count = 0

    async for item in cursor:
        old_path = item.get("physical_path")
        item_id = item.get("_id")

        # Extract just the filename — directory structure is changing
        filename = os.path.basename(old_path)
        source_path = os.path.join(OLD_FILES_DIR, filename)
        target_path = os.path.join(NEW_FILES_DIR, filename)

        print(f"[*] Migrating item {item.get('name')} (ID: {item_id})...")

        if os.path.exists(source_path):
            try:
                # Hash and measure before moving so we capture the original file
                file_hash = await calculate_hash(source_path)
                file_size = os.path.getsize(source_path)

                shutil.move(source_path, target_path)
                print(f"    [+] Moved physical file to storage node.")

                # Replace the old path field with the new distributed-storage fields
                await items.update_one(
                    {"_id": item_id},
                    {
                        "$set": {
                            "physical_name": filename,
                            "file_hash": file_hash,
                            "size": file_size,
                            "status": "completed"
                        },
                        "$unset": {"physical_path": ""}
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
