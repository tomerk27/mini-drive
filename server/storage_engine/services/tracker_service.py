from common.database import get_collection
from common.utils.node_utils import NodeStatus
from datetime import timedelta
from common.utils.time import current_time

class TrackerService:
    @staticmethod
    async def update_node_status(node_id: str, ip: str, port: int, capacity: int):
        """Upserts a node's heartbeat data into MongoDB."""
        nodes_collection = get_collection("nodes")

        await nodes_collection.update_one(
            {"node_id": node_id},
            {
                "$set": {
                    "ip": ip,
                    "port": port,
                    "available_capacity": capacity,
                    "status": NodeStatus.ONLINE,
                    "last_heartbeat": current_time()
                }
            },
            upsert=True
        )
        print(f"[*] Tracker: Registered heartbeat for {node_id} ({ip}:{port}) - {capacity} bytes free")

    @staticmethod
    async def select_best_nodes(limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        """
        Selects the best online nodes, optionally excluding specific nodes (e.g., ones that already have the file).
        """
        nodes_collection = get_collection("nodes")
        active_threshold = current_time() - timedelta(minutes=2)
        
        query = {
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$gt": active_threshold}
        }
        
        if exclude_node_ids:
            # Exclude nodes that are already in the provided list
            query["node_id"] = {"$nin": exclude_node_ids}
   
        cursor = nodes_collection.find(query).sort("available_capacity", -1).limit(limit)
        nodes = await cursor.to_list(length=limit)
        
        return [node["node_id"] for node in nodes]
    
    @staticmethod
    async def check_dead_nodes() -> list[str]:
        """Identifies dead nodes, marks them OFFLINE, and triggers repair logic."""
        nodes_collection = get_collection("nodes")
        active_threshold = current_time() - timedelta(minutes=2)

        cursor = nodes_collection.find({
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$lt": active_threshold}
        })

        dead_nodes = await cursor.to_list(length=100)
        if not dead_nodes:
            return []

        dead_node_ids = [node["node_id"] for node in dead_nodes]

        # 1. Update status to OFFLINE in bulk
        await nodes_collection.update_many(
            {"node_id": {"$in": dead_node_ids}},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

        # 2. Trigger Repair logic for each dead node
        # Defer import to avoid circular dependency
        from web_api.services.repair_service import RepairService
        
        for node_id in dead_node_ids:
            print(f"[!] Tracker: Node {node_id} marked OFFLINE. Triggering repair...")
            await RepairService.handle_node_failure(node_id)

        return dead_node_ids
