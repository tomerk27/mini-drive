"""
Time utilities — returns timezone-aware datetimes for consistent DB timestamps.
"""

from datetime import datetime
from zoneinfo import ZoneInfo


def current_time() -> datetime:
    """
    Returns the current time in the Asia/Jerusalem timezone.

    All created_at and last_heartbeat fields use this so timestamps
    are consistent regardless of where the server is running.
    """
    return datetime.now(ZoneInfo("Asia/Jerusalem"))