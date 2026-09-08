from dataclasses import dataclass
import importlib
from typing import Any


@dataclass(frozen=True)
class FaceBox:
    x: int
    y: int
    width: int
    height: int
    confidence: float = 1.0


class FaceDetector:
    def detect(self, frame: Any) -> list[FaceBox]:
        """Return OpenCV Haar detections when available, otherwise an empty result."""
        try:
            cv2: Any = importlib.import_module("cv2")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            return [FaceBox(int(x), int(y), int(width), int(height)) for x, y, width, height in classifier.detectMultiScale(gray)]
        except Exception:
            return []