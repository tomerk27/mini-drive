import io
from common import get_collection, ItemType
from storage_engine.services.tracker_service import TrackerService
from storage_engine import get_file_from_storage, send_file_to_storage

class RepairService:
    @staticmethod
    async def handle_node_failure(dead_node_id: str):
        """Phase 2: Finds all files that were stored on the dead node."""
        items_collection = get_collection("items")

        # Find files that contain this dead_node_id in their node_ids list
        cursor = items_collection.find({
            "item_type": ItemType.FILE,
            "node_ids": dead_node_id
        })

        async for item in cursor:
            # Delegate to the "Planner"
            await RepairService.repair_item(item, dead_node_id)

    @staticmethod
    async def repair_item(item: dict, dead_node_id: str):
        """Intermediate Function: Plans the repair for a single item."""
        node_ids = item.get("node_ids", [])
        
        # 1. Identify surviving nodes (Source candidates)
        survivors = [nid for nid in node_ids if nid != dead_node_id]
        if not survivors:
            print(f"[!] Critical: No surviving nodes for file {item.get('name')}")
            return

        # 2. Ask Tracker for 1 healthy node that DOES NOT already have this file
        # This uses the improved Tracker logic to handle exclusion at the DB level
        target_candidates = await TrackerService.select_best_nodes(limit=1, exclude_node_ids=node_ids)

        if not target_candidates:
            print(f"[!] Warning: No healthy nodes available to host a new replica for {item.get('name')}")
            return

        source_node = survivors[0]
        target_node = target_candidates[0]
        
        await RepairService.replicate_file(item, source_node, target_node, dead_node_id)

    @staticmethod
    async def replicate_file(item: dict, source_node: str, target_node: str, dead_node: str):
        """Phase 3: The Executor. Moves the bits and updates the DB."""
        items_collection = get_collection("items")
        
        try:
            # 1. Download from source (Buffer into BytesIO for seekability)
            file_gen = get_file_from_storage(source_node, item["physical_name"], item["file_hash"])
            
            buffer = io.BytesIO()
            for chunk in file_gen:
                buffer.write(chunk)
            buffer.seek(0)

            # 2. Upload to the new target node
            # We wrap the node in a list because send_file_to_storage expects list[str]
            success, _ = send_file_to_storage([target_node], item["physical_name"], item["size"], buffer)

            if success:
                # 3. Update DB: Remove dead node, Add new target node
                await items_collection.update_one(
                    {"_id": item["_id"]},
                    {
                        "$pull": {"node_ids": dead_node},
                        "$addToSet": {"node_ids": target_node}
                    }
                )
                print(f"[+] Successfully repaired {item['name']} from {source_node} to {target_node}")
            else:
                print(f"[!] Failed to upload replica of {item['name']} to {target_node}")

        except Exception as e:
            print(f"[!] Error during replication of {item['name']}: {e}")
