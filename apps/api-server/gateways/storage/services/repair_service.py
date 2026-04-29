"""
Self-healing repair logic: re-replicates file chunks after a node goes offline.

Called by the NodeMonitor whenever dead nodes are detected. The repair
strategy is: download the chunk from a surviving replica, upload it to a
fresh healthy node, then update the DB to replace the dead node ID.
"""

import io
from gateways.database.repositories.item_repository import item_repository
from core.enums import ItemType
from gateways.storage.services.node_registry import NodeRegistry
from gateways.storage.services.node_distribution_service import get_file_from_node, send_file_to_nodes


class RepairService:
    """
    Handles file replication when a storage node goes offline.

    Works at the chunk level: for each chunk that was stored on the dead node,
    it finds a surviving replica, downloads the data, uploads it to a new node,
    and updates the DB. This keeps the 3-replica invariant intact.
    """

    @staticmethod
    def handle_node_failure(dead_node_id: str):
        """
        Entry point for repairing all files affected by a dead node.

        Args:
            dead_node_id: The ID of the node that just went offline.
        """
        affected_items = item_repository.get_files_on_node(dead_node_id)
        for item in affected_items:
            RepairService._repair_item(item, dead_node_id)

    @staticmethod
    def _repair_item(item, dead_node_id: str):
        """Iterates a file's chunks and repairs any that were on the dead node."""
        for chunk_info in item.chunks:
            if dead_node_id in chunk_info.node_ids:
                RepairService._repair_chunk(item, chunk_info, dead_node_id)

    @staticmethod
    def _repair_chunk(item, chunk_info, dead_node_id: str):
        """
        Re-replicates one chunk from a surviving node to a new healthy node.

        Args:
            item: The FileModel that owns this chunk.
            chunk_info: Metadata for the specific chunk being repaired.
            dead_node_id: The node that died (to exclude from survivor list).
        """
        # Identify which replicas are still alive for this chunk.
        survivors = [nid for nid in chunk_info.node_ids if nid != dead_node_id]

        if not survivors:
            print(f"[!] RepairService: No surviving nodes for chunk {chunk_info.chunk_index} of '{item.name}' — data lost")
            return

        # Find a new node to receive the copy, excluding all current replicas
        # (including the dead one) to avoid writing to a node already holding it.
        target_candidates = NodeRegistry.select_best_nodes(limit=1, exclude_node_ids=chunk_info.node_ids)
        if not target_candidates:
            print(f"[!] RepairService: No healthy target node available for chunk {chunk_info.chunk_index} of '{item.name}'")
            return

        target_node = target_candidates[0]
        try:
            # Download from the first surviving replica (integrity-checked via hash).
            data = get_file_from_node(survivors[0], chunk_info.physical_name, chunk_info.chunk_hash)

            success, _ = send_file_to_nodes([target_node], chunk_info.physical_name, chunk_info.size, io.BytesIO(data))

            if success:
                # Update the DB to swap the dead node for the new one.
                item_repository.replace_node_in_chunk(str(item.id), chunk_info.physical_name, dead_node_id, target_node)
                print(f"[+] RepairService: Repaired chunk {chunk_info.chunk_index} of '{item.name}' — {survivors[0]} → {target_node}")
            else:
                print(f"[!] RepairService: Upload failed for chunk {chunk_info.chunk_index} of '{item.name}' to {target_node}")

        except Exception as e:
            print(f"[!] RepairService: Error replicating chunk {chunk_info.chunk_index} of '{item.name}': {e}")
