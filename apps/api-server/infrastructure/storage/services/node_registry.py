from infrastructure.database.database import get_collection
from core.enums import NodeStatus
from datetime import timedelta
from utils.time import current_time


class NodeRegistry:
    """
    Manages storage node state: registration via heartbeats, health queries,
    and node selection for file placement.

    Repair orchestration is intentionally NOT here — see workers/node_monitor.py.
    """

    @staticmethod
    async def update_node_status(node_id: str, ip: str, port: int, capacity: int):
        """Upserts a node's heartbeat data into the database."""
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
        print(f"[*] NodeRegistry: Heartbeat from {node_id} ({ip}:{port}) — {capacity} bytes free")

    @staticmethod
    async def select_best_nodes(limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        """
        Returns up to `limit` online node IDs sorted by available capacity.
        Optionally excludes nodes that already hold a copy of the file.
        """
        nodes_collection = get_collection("nodes")
        active_threshold = current_time() - timedelta(minutes=2)

        query = {
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$gt": active_threshold}
        }

        if exclude_node_ids:
            query["node_id"] = {"$nin": exclude_node_ids}

        cursor = nodes_collection.find(query).sort("available_capacity", -1).limit(limit)
        nodes = await cursor.to_list(length=limit)

        return [node["node_id"] for node in nodes]

    @staticmethod
    async def mark_dead_nodes() -> list[str]:
        """
        Finds nodes that have missed their heartbeat window, marks them OFFLINE,
        and returns their IDs so the caller can trigger repair logic.
        """
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

        await nodes_collection.update_many(
            {"node_id": {"$in": dead_node_ids}},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

        for node_id in dead_node_ids:
            print(f"[!] NodeRegistry: Node {node_id} marked OFFLINE")

        return dead_node_ids
