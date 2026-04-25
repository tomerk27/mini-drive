import time
from gateways.storage.services.node_registry import NodeRegistry
from gateways.storage.services.repair_service import RepairService

HEALTH_CHECK_INTERVAL_SECONDS = 60


def run_node_monitor():
    """
    Background worker that periodically checks for dead storage nodes and
    triggers re-replication for any files they were holding.
    Runs in a daemon thread started at application startup.
    """
    print("[*] NodeMonitor: Started — checking node health every "
          f"{HEALTH_CHECK_INTERVAL_SECONDS}s")

    while True:
        try:
            dead_node_ids = NodeRegistry.mark_dead_nodes()
            for node_id in dead_node_ids:
                print(f"[!] NodeMonitor: Triggering repair for dead node {node_id}")
                RepairService.handle_node_failure(node_id)
        except Exception as e:
            print(f"[!] NodeMonitor Error: {e}")

        time.sleep(HEALTH_CHECK_INTERVAL_SECONDS)
