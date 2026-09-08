from collections.abc import Iterator
import importlib
from typing import Any


class CameraStream:
    """Best-effort frame source; returns no frames when OpenCV/source is unavailable."""

    def __init__(self, source: str = "0") -> None:
        self.source = int(source) if source.isdigit() else source
        self._capture: Any = None

    def start(self) -> "CameraStream":
        try:
            cv2: Any = importlib.import_module("cv2")
            self._capture = cv2.VideoCapture(self.source)
        except Exception:
            self._capture = None
        return self

    def frames(self) -> Iterator[Any]:
        while self._capture is not None and self._capture.isOpened():
            success, frame = self._capture.read()
            if not success:
                break
            yield frame

    def stop(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None