"""
Service layer facade over NodeRepository — used by the HeartbeatServer,
upload logic, and NodeMonitor to interact with storage node state.
"""

from gateways.database.repositories.node_repository import node_repository


class NodeRegistry:
    """
    Manages storage node state: registration via heartbeats, health queries,
    and node selection for file placement.

    Acts as a thin service layer so callers don't import the repository directly.
    """

    @staticmethod
    def update_node_status(node_id: str, ip: str, port: int, capacity: int):
        """
        Records a heartbeat from a storage node, creating the node record if new.

        Args:
            node_id: Unique identifier for the node.
            ip: Source IP of the heartbeat connection.
            port: Port the node is listening on for file commands.
            capacity: Free disk space in bytes reported by the node.
        """
        node_repository.upsert_heartbeat(node_id, ip, port, capacity)
        print(f"[*] NodeRegistry: Heartbeat from {node_id} ({ip}:{port}) — {capacity} bytes free")

    @staticmethod
    def select_best_nodes(limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        """
        Returns the IDs of the healthiest nodes available for storing a chunk.

        Args:
            limit: How many nodes to return (default 3 for 3-way replication).
            exclude_node_ids: Nodes to skip (e.g. already holding a previous chunk).

        Returns:
            List of node ID strings ordered by free space (most free first).
        """
        return node_repository.get_best_nodes(limit=limit, exclude_node_ids=exclude_node_ids)

    @staticmethod
    def mark_dead_nodes() -> list[str]:
        """
        Detects nodes that have missed their heartbeat window and marks them OFFLINE.

        Returns:
            List of node IDs that were just marked dead (used to trigger repair).
        """
        dead_node_ids = node_repository.get_dead_nodes()

        for node_id in dead_node_ids:
            print(f"[!] NodeRegistry: Node {node_id} marked OFFLINE")

        return dead_node_ids
