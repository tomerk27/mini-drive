from common import get_collection
from common.utils.node_utils import NodeStatus
from datetime import datetime, timedelta
from common import current_time

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
    async def select_best_node() -> str:
        """Selects the online node with the most available capacity."""
        nodes_collection = get_collection("nodes")
        
        # Consider nodes active if heartbeat within last 2 minutes
        active_threshold = current_time() - timedelta(minutes=2)
        
        cursor = nodes_collection.find({
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$gt": active_threshold}
        }).sort("available_capacity", -1).limit(1)
        
        node = await cursor.to_list(length=1)
        if node:
            return node[0]["node_id"]
        return None
