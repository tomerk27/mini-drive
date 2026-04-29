"""
Background worker that drives the self-healing loop.
Runs every 60 seconds: finds nodes that stopped sending heartbeats,
marks them OFFLINE, and triggers re-replication for every file they held.
"""

import time
from gateways.storage.services.node_registry import NodeRegistry
from gateways.storage.services.repair_service import RepairService

# How often (in seconds) to scan for dead nodes.
# A node is considered dead if it has been silent for more than 2 minutes,
# so this interval gives roughly one check per missed-heartbeat window.
HEALTH_CHECK_INTERVAL_SECONDS = 60


def run_node_monitor():
    """
    Runs the node health check loop forever in a background daemon thread.

    On each tick, it asks NodeRegistry which nodes have gone silent, then
    tells RepairService to re-replicate every file those nodes were holding.
    Errors are caught and logged so a single bad cycle never stops the loop.
    """
    print("[*] NodeMonitor: Started — checking node health every "
          f"{HEALTH_CHECK_INTERVAL_SECONDS}s")

    while True:
        try:
            # Mark silent nodes OFFLINE and get their IDs so we know what to repair.
            dead_node_ids = NodeRegistry.mark_dead_nodes()

            for node_id in dead_node_ids:
                print(f"[!] NodeMonitor: Triggering repair for dead node {node_id}")
                # Download each affected chunk from a surviving replica and
                # upload it to a new healthy node to restore 3-way replication.
                RepairService.handle_node_failure(node_id)

        except Exception as e:
            # Log and continue — a crash here would silently stop self-healing.
            print(f"[!] NodeMonitor Error: {e}")

        time.sleep(HEALTH_CHECK_INTERVAL_SECONDS)
