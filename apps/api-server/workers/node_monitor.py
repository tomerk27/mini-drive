import asyncio
from infrastructure.storage.services.node_registry import NodeRegistry
from infrastructure.storage.services.repair_service import RepairService

HEALTH_CHECK_INTERVAL_SECONDS = 60


async def run_node_monitor():
    """
    Background worker that periodically checks for dead storage nodes and
    triggers re-replication for any files they were holding.

    Orchestrates NodeRegistry (detection) and RepairService (recovery) so
    neither needs to know about the other.
    """
    print("[*] NodeMonitor: Started — checking node health every "
          f"{HEALTH_CHECK_INTERVAL_SECONDS}s")

    while True:
        try:
            dead_node_ids = await NodeRegistry.mark_dead_nodes()
            for node_id in dead_node_ids:
                print(f"[!] NodeMonitor: Triggering repair for dead node {node_id}")
                await RepairService.handle_node_failure(node_id)
        except Exception as e:
            print(f"[!] NodeMonitor Error: {e}")

        await asyncio.sleep(HEALTH_CHECK_INTERVAL_SECONDS)
