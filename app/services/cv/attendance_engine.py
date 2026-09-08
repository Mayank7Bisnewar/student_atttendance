import time


class AttendanceDebouncer:
    def __init__(self, cooldown_seconds: float = 30.0) -> None:
        self.cooldown_seconds = cooldown_seconds
        self._last_seen: dict[tuple[str, str], float] = {}

    def should_record(self, session_id: str, student_id: str, now: float | None = None) -> bool:
        current = time.monotonic() if now is None else now
        key = (session_id, student_id)
        previous = self._last_seen.get(key)
        if previous is not None and current - previous < self.cooldown_seconds:
            return False
        self._last_seen[key] = current
        return True