from gateways.database.repositories.node_repository import node_repository


class NodeRegistry:
    """
    Manages storage node state: registration via heartbeats, health queries,
    and node selection for file placement.
    """

    @staticmethod
    def update_node_status(node_id: str, ip: str, port: int, capacity: int):
        node_repository.upsert_heartbeat(node_id, ip, port, capacity)
        print(f"[*] NodeRegistry: Heartbeat from {node_id} ({ip}:{port}) — {capacity} bytes free")

    @staticmethod
    def select_best_nodes(limit: int = 3, exclude_node_ids: list[str] = None) -> list[str]:
        return node_repository.get_best_nodes(limit=limit, exclude_node_ids=exclude_node_ids)

    @staticmethod
    def mark_dead_nodes() -> list[str]:
        dead_node_ids = node_repository.get_dead_nodes()

        for node_id in dead_node_ids:
            print(f"[!] NodeRegistry: Node {node_id} marked OFFLINE")

        return dead_node_ids
