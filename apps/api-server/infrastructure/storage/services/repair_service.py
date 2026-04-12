import io
from infrastructure.database.repositories.item_repository import item_repository
from core.enums import ItemType
from infrastructure.storage.services.node_registry import NodeRegistry
from infrastructure.storage.services.node_distribution_service import get_file_from_node, send_file_to_nodes


class RepairService:
    """
    Handles file replication when a storage node goes offline.
    Called by the node monitor after dead nodes are detected.
    """

    @staticmethod
    async def handle_node_failure(dead_node_id: str):
        """Finds all files stored on the dead node and schedules re-replication."""
        affected_items = await item_repository.get_files_on_node(dead_node_id)

        for item in affected_items:
            await RepairService._repair_item(item, dead_node_id)

    @staticmethod
    async def _repair_item(item, dead_node_id: str):
        """Plans the repair for a single item: picks a source and a target node."""
        node_ids = item.node_ids or []
        survivors = [nid for nid in node_ids if nid != dead_node_id]

        if not survivors:
            print(f"[!] RepairService: No surviving nodes for '{item.name}' — data lost")
            return

        target_candidates = await NodeRegistry.select_best_nodes(limit=1, exclude_node_ids=node_ids)
        if not target_candidates:
            print(f"[!] RepairService: No healthy target node available for '{item.name}'")
            return

        await RepairService._replicate_file(item, source_node=survivors[0], target_node=target_candidates[0], dead_node=dead_node_id)

    @staticmethod
    async def _replicate_file(item, source_node: str, target_node: str, dead_node: str):
        """Downloads from the source node and re-uploads to the target node, then updates the DB."""
        try:
            file_gen = await get_file_from_node(source_node, item.physical_name, item.file_hash)

            buffer = io.BytesIO()
            async for chunk in file_gen:
                buffer.write(chunk)
            buffer.seek(0)

            success, _ = await send_file_to_nodes([target_node], item.physical_name, item.size, buffer)

            if success:
                await item_repository.replace_node(str(item.id), dead_node, target_node)
                print(f"[+] RepairService: Repaired '{item.name}' — {source_node} → {target_node}")
            else:
                print(f"[!] RepairService: Upload failed for '{item.name}' to {target_node}")

        except Exception as e:
            print(f"[!] RepairService: Error replicating '{item.name}': {e}")
