from bson import ObjectId
from typing import Optional
from datetime import datetime, timedelta
from gateways.database.database import get_collection
from models.node import StorageNodeModel
from core.enums import NodeStatus
from utils.time import current_time


class NodeRepository:
    def __init__(self):
        self.collection = get_collection("nodes")

    async def upsert_heartbeat(self, node_id: str, ip: str, port: int, capacity: int):
        """Inserts or updates a node's heartbeat data."""
        await self.collection.update_one(
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

    async def get_best_nodes(self, limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        """Returns up to `limit` online node IDs sorted by available capacity."""
        active_threshold = current_time() - timedelta(minutes=2)

        query = {
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$gt": active_threshold}
        }

        if exclude_node_ids:
            query["node_id"] = {"$nin": exclude_node_ids}

        cursor = self.collection.find(query).sort("available_capacity", -1).limit(limit)
        nodes = await cursor.to_list(length=limit)
        return [node["node_id"] for node in nodes]

    async def get_by_id(self, node_id: str) -> Optional[StorageNodeModel]:
        raw = await self.collection.find_one({"node_id": node_id})
        if not raw:
            return None
        raw["id"] = str(raw["_id"])
        return StorageNodeModel(**raw)

    async def mark_offline(self, node_id: str):
        """Sets a node's status to OFFLINE."""
        await self.collection.update_one(
            {"node_id": node_id},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

    async def get_dead_nodes(self) -> list[str]:
        """Returns IDs of online nodes that missed their heartbeat window, and marks them OFFLINE."""
        active_threshold = current_time() - timedelta(minutes=2)

        cursor = self.collection.find({
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$lt": active_threshold}
        })

        dead_nodes = await cursor.to_list(length=100)
        if not dead_nodes:
            return []

        dead_node_ids = [node["node_id"] for node in dead_nodes]

        await self.collection.update_many(
            {"node_id": {"$in": dead_node_ids}},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

        return dead_node_ids


node_repository = NodeRepository()
