import io
from gateways.database.repositories.item_repository import item_repository
from core.enums import ItemType
from gateways.storage.services.node_registry import NodeRegistry
from gateways.storage.services.node_distribution_service import get_file_from_node, send_file_to_nodes


class RepairService:
    """
    Handles file replication when a storage node goes offline.
    Called by the node monitor after dead nodes are detected.
    """

    @staticmethod
    async def handle_node_failure(dead_node_id: str):
        """Finds all files with chunks on the dead node and repairs each affected chunk."""
        affected_items = await item_repository.get_files_on_node(dead_node_id)

        for item in affected_items:
            await RepairService._repair_item(item, dead_node_id)

    @staticmethod
    async def _repair_item(item, dead_node_id: str):
        """Iterates a file's chunks and repairs any that were stored on the dead node."""
        for chunk_info in item.chunks:
            if dead_node_id in chunk_info.node_ids:
                await RepairService._repair_chunk(item, chunk_info, dead_node_id)

    @staticmethod
    async def _repair_chunk(item, chunk_info, dead_node_id: str):
        """Downloads a chunk from a surviving replica and re-uploads it to a new healthy node."""
        survivors = [nid for nid in chunk_info.node_ids if nid != dead_node_id]

        if not survivors:
            print(f"[!] RepairService: No surviving nodes for chunk {chunk_info.chunk_index} of '{item.name}' — data lost")
            return

        target_candidates = await NodeRegistry.select_best_nodes(limit=1, exclude_node_ids=chunk_info.node_ids)
        if not target_candidates:
            print(f"[!] RepairService: No healthy target node available for chunk {chunk_info.chunk_index} of '{item.name}'")
            return

        target_node = target_candidates[0]
        try:
            file_gen = await get_file_from_node(survivors[0], chunk_info.physical_name, chunk_info.chunk_hash)

            buffer = io.BytesIO()
            async for data in file_gen:
                buffer.write(data)
            buffer.seek(0)

            success, _ = await send_file_to_nodes([target_node], chunk_info.physical_name, chunk_info.size, buffer)

            if success:
                await item_repository.replace_node_in_chunk(str(item.id), chunk_info.physical_name, dead_node_id, target_node)
                print(f"[+] RepairService: Repaired chunk {chunk_info.chunk_index} of '{item.name}' — {survivors[0]} → {target_node}")
            else:
                print(f"[!] RepairService: Upload failed for chunk {chunk_info.chunk_index} of '{item.name}' to {target_node}")

        except Exception as e:
            print(f"[!] RepairService: Error replicating chunk {chunk_info.chunk_index} of '{item.name}': {e}")
