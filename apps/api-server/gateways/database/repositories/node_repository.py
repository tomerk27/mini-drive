"""
Data access layer for the 'nodes' MongoDB collection.

Tracks storage node registration, heartbeat timestamps, and health status.
"""

from typing import Optional
from datetime import timedelta
from gateways.database.database import get_collection
from models.node import StorageNodeModel
from core.enums import NodeStatus
from utils.time import current_time


class NodeRepository:
    """
    Handles reads and writes to the 'nodes' collection.

    A node is considered alive if it sent a heartbeat within the last 2 minutes.
    Any node that misses that window is treated as dead and flagged for repair.
    """

    def __init__(self):
        self.collection = get_collection("nodes")

    def upsert_heartbeat(self, node_id: str, ip: str, port: int, capacity: int):
        """
        Creates or updates the node's DB record when a heartbeat arrives.

        Uses upsert=True so the first heartbeat from a new node automatically
        registers it without a separate registration step.

        Args:
            node_id: Unique identifier for the node.
            ip: The IP address the heartbeat was received from.
            port: The port the node is listening on for file commands.
            capacity: Free disk space in bytes at the time of the heartbeat.
        """
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
        """
        Returns IDs of the healthiest nodes, sorted by available capacity (most free first).

        Only considers nodes that are ONLINE and sent a heartbeat within the last 2 minutes.

        Args:
            limit: Maximum number of node IDs to return (default 3 for replication).
            exclude_node_ids: Optional list of node IDs to skip (e.g. nodes already
                holding a previous chunk of the same file).

        Returns:
            List of node ID strings, up to `limit` entries.
        """
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
        """Fetches a single node's full record. Returns None if not found."""
        raw = self.collection.find_one({"node_id": node_id})
        if not raw:
            return None
        raw["id"] = str(raw["_id"])
        return StorageNodeModel(**raw)

    def mark_offline(self, node_id: str):
        """Marks a specific node as OFFLINE without waiting for a missed heartbeat."""
        self.collection.update_one(
            {"node_id": node_id},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

    def get_dead_nodes(self) -> list[str]:
        """
        Finds nodes that are still marked ONLINE but haven't heartbeated in 2+ minutes,
        marks them OFFLINE in the database, and returns their IDs.

        This is called by the NodeMonitor every 60 seconds. Doing the status update
        here (rather than in the caller) ensures the DB is updated atomically with
        the dead-node detection, preventing double-repair on the next cycle.
        """
        active_threshold = current_time() - timedelta(minutes=2)

        dead_nodes = list(self.collection.find({
            "status": NodeStatus.ONLINE,
            "last_heartbeat": {"$lt": active_threshold}
        }))

        if not dead_nodes:
            return []

        dead_node_ids = [node["node_id"] for node in dead_nodes]

        # Mark all dead nodes OFFLINE in one bulk operation.
        self.collection.update_many(
            {"node_id": {"$in": dead_node_ids}},
            {"$set": {"status": NodeStatus.OFFLINE}}
        )

        return dead_node_ids


# Singleton instance used across the entire API server process.
node_repository = NodeRepository()
