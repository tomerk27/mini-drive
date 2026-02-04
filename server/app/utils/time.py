from datetime import datetime
from zoneinfo import ZoneInfo

def current_time():
    return datetime.now(ZoneInfo("Asia/Jerusalem"))