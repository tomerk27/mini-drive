import shutil
from app.core.config import settings

class SystemMetricsService:
    @staticmethod
    def get_free_space() -> int:
        """Calculates the available free space in bytes in the storage directory."""
        return shutil.disk_usage(settings.STORAGE_DIR).free