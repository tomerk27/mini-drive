import asyncio
import hashlib
import io
import uuid

from infrastructure.database.database import get_collection
from infrastructure.storage.servers.connection_pool import connection_pool
from infrastructure.storage.services.node_distribution_service import get_file_from_node, delete_file_from_node
from infrastructure.storage.services.node_registry import NodeRegistry
from infrastructure.storage.client.storage_client import StorageClient
from core.config import settings
from core.enums import ItemType


async def _wait_for_nodes():
    """Blocks until at least one storage node is connected to the pool."""
    print("[*] MigrationWorker: Waiting for storage nodes to connect...")
    while not connection_pool.connections:
        await asyncio.sleep(5)
    print(f"[*] MigrationWorker: {len(connection_pool.connections)} node(s) connected. Starting migration.")


async def _upload_chunk_to_node(node_id: str, physical_name: str, chunk_size: int, chunk_data: bytes) -> bool:
    try:
        client = StorageClient(node_id=node_id, encryption_key=settings.STORAGE_ENCRYPTION_KEY.encode())
        return await client.upload(physical_name, chunk_size, io.BytesIO(chunk_data))
    except Exception as e:
        print(f"[!] MigrationWorker: Upload to {node_id} failed: {e}")
        return False


async def _migrate_file(collection, doc: dict):
    item_id = doc["_id"]
    name = doc.get("name", str(item_id))
    physical_name = doc.get("physical_name")
    old_node_ids = doc.get("node_ids", [])
    old_file_hash = doc.get("file_hash")

    if not old_node_ids or not physical_name:
        print(f"[!] MigrationWorker: Skipping '{name}' — missing physical_name or node_ids")
        return

    print(f"[*] MigrationWorker: Migrating '{name}'...")

    # Download full file from first node
    try:
        file_gen = await get_file_from_node(old_node_ids[0], physical_name, old_file_hash)
        buffer = io.BytesIO()
        async for data in file_gen:
            buffer.write(data)
        file_content = buffer.getvalue()
    except Exception as e:
        print(f"[!] MigrationWorker: Failed to download '{name}': {e}")
        return

    # Split into chunks
    chunk_size_bytes = settings.CHUNK_SIZE_BYTES
    raw_chunks = [
        file_content[i:i + chunk_size_bytes]
        for i in range(0, len(file_content), chunk_size_bytes)
    ]
    base_uuid = str(uuid.uuid4()).replace("-", "")

    # Upload each chunk to 3 nodes concurrently, rotating the primary node
    chunks = []
    last_primary: list[str] = []

    for i, chunk_data in enumerate(raw_chunks):
        node_ids = await NodeRegistry.select_best_nodes(limit=3, exclude_node_ids=last_primary or None)
        if not node_ids:
            node_ids = await NodeRegistry.select_best_nodes(limit=3)
        if not node_ids:
            print(f"[!] MigrationWorker: No nodes available for chunk {i} of '{name}'")
            return
        last_primary = [node_ids[0]]

        physical_chunk_name = f"{base_uuid}_{i}"
        chunk_hash = hashlib.sha256(chunk_data).hexdigest()

        results = await asyncio.gather(*[
            _upload_chunk_to_node(nid, physical_chunk_name, len(chunk_data), chunk_data)
            for nid in node_ids
        ])
        succeeded = [node_ids[j] for j, ok in enumerate(results) if ok]

        if not succeeded:
            print(f"[!] MigrationWorker: All uploads failed for chunk {i} of '{name}'")
            return

        chunks.append({
            "chunk_index": i,
            "size": len(chunk_data),
            "chunk_hash": chunk_hash,
            "physical_name": physical_chunk_name,
            "node_ids": succeeded,
        })

    # Compute new file_hash from chunk hashes
    new_file_hash = hashlib.sha256("".join(c["chunk_hash"] for c in chunks).encode()).hexdigest()

    # Update MongoDB: replace old fields with chunks
    await collection.update_one(
        {"_id": item_id},
        {
            "$set": {"chunks": chunks, "file_hash": new_file_hash},
            "$unset": {"physical_name": "", "node_ids": ""}
        }
    )

    # Delete old full file from all original nodes
    for node_id in old_node_ids:
        await delete_file_from_node(node_id, physical_name)

    print(f"[+] MigrationWorker: '{name}' migrated to {len(chunks)} chunk(s).")


async def run_migration():
    """
    One-time migration: converts all files stored as full files into chunks.
    Runs at startup after storage nodes have connected.
    """
    await _wait_for_nodes()

    collection = get_collection("items")

    # Find files with the old schema (have physical_name, no chunks array)
    cursor = collection.find({
        "item_type": ItemType.FILE,
        "physical_name": {"$exists": True},
    })
    old_files = await cursor.to_list(length=None)

    if not old_files:
        print("[*] MigrationWorker: No files to migrate.")
        return

    print(f"[*] MigrationWorker: Found {len(old_files)} file(s) to migrate.")

    for doc in old_files:
        await _migrate_file(collection, doc)

    print("[+] MigrationWorker: Migration complete.")
