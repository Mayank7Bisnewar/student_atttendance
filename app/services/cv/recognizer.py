from math import sqrt


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


class FaceRecognizer:
    def __init__(self, threshold: float = 0.65) -> None:
        self.threshold = threshold

    def match(self, embedding: list[float], candidates: dict[str, list[float]]) -> tuple[str | None, float]:
        matches = [(student_id, cosine_similarity(embedding, known)) for student_id, known in candidates.items()]
        if not matches:
            return None, 0.0
        student_id, score = max(matches, key=lambda item: item[1])
        return (student_id, score) if score >= self.threshold else (None, score)