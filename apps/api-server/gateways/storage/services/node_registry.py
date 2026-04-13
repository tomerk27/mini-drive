from gateways.database.repositories.node_repository import node_repository


class NodeRegistry:
    """
    Manages storage node state: registration via heartbeats, health queries,
    and node selection for file placement.

    Repair orchestration is intentionally NOT here — see workers/node_monitor.py.
    """

    @staticmethod
    async def update_node_status(node_id: str, ip: str, port: int, capacity: int):
        """Upserts a node's heartbeat data into the database."""
        await node_repository.upsert_heartbeat(node_id, ip, port, capacity)
        print(f"[*] NodeRegistry: Heartbeat from {node_id} ({ip}:{port}) — {capacity} bytes free")

    @staticmethod
    async def select_best_nodes(limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        """
        Returns up to `limit` online node IDs sorted by available capacity.
        Optionally excludes nodes that already hold a copy of the file.
        """
        return await node_repository.get_best_nodes(limit=limit, exclude_node_ids=exclude_node_ids)

    @staticmethod
    async def mark_dead_nodes() -> list[str]:
        """
        Finds nodes that have missed their heartbeat window, marks them OFFLINE,
        and returns their IDs so the caller can trigger repair logic.
        """
        dead_node_ids = await node_repository.get_dead_nodes()

        for node_id in dead_node_ids:
            print(f"[!] NodeRegistry: Node {node_id} marked OFFLINE")

        return dead_node_ids
