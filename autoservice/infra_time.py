from datetime import datetime
from .interfaces import TimeProvider

class SystemTime(TimeProvider):
    def now(self) -> datetime:
        return datetime.now()
