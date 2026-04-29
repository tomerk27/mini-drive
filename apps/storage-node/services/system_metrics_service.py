"""
system_metrics_service.py

Provides a simple utility for reading local disk metrics on this storage node.
Used by the heartbeat sender to report available capacity to the API server.
"""

import shutil
from core.config import settings


class SystemMetricsService:
    """
    Reads hardware/OS-level metrics for this storage node.

    Currently only exposes free disk space, which is included in every
    heartbeat packet so the API server can pick the least-full nodes
    when distributing new file uploads.
    """

    @staticmethod
    def get_free_space() -> int:
        """
        Returns the free disk space available in the storage directory.

        Returns:
            Free bytes available on the partition that holds STORAGE_DIR.
        """
        return shutil.disk_usage(settings.STORAGE_DIR).free
