from typing import Optional
from datetime import timedelta
from gateways.database.database import get_collection
from models.node import StorageNodeModel
from core.enums import NodeStatus
from utils.time import current_time


class NodeRepository:
    def __init__(self):
        self.collection = get_collection("nodes")

    def upsert_heartbeat(self, node_id: str, ip: str, port: int, capacity: int):
        self.collection.update_one(
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

    def get_best_nodes(self, limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        active_threshold = current_time() - timedelta(minutes=2)

        query = {
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$gt": active_threshold}
        }

        if exclude_node_ids:
            query["node_id"] = {"$nin": exclude_node_ids}

        cursor = self.collection.find(query).sort("available_capacity", -1).limit(limit)
        return [node["node_id"] for node in cursor]

    def get_by_id(self, node_id: str) -> Optional[StorageNodeModel]:
        raw = self.collection.find_one({"node_id": node_id})
        if not raw:
            return None
        raw["id"] = str(raw["_id"])
        return StorageNodeModel(**raw)

    def mark_offline(self, node_id: str):
        self.collection.update_one(
            {"node_id": node_id},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

    def get_dead_nodes(self) -> list[str]:
        active_threshold = current_time() - timedelta(minutes=2)

        dead_nodes = list(self.collection.find({
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$lt": active_threshold}
        }))

        if not dead_nodes:
            return []

        dead_node_ids = [node["node_id"] for node in dead_nodes]

        self.collection.update_many(
            {"node_id": {"$in": dead_node_ids}},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

        return dead_node_ids


node_repository = NodeRepository()
