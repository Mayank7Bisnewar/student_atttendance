from fastapi.testclient import TestClient

from main import app
from app.core.security import hash_password
from app.services.cv.attendance_engine import AttendanceDebouncer
from app.services.cv.recognizer import FaceRecognizer


def test_health_and_student_crud() -> None:
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        response = client.post("/api/v1/students", json={"name": "Asha", "roll_no": "1", "class_name": "CSE"})
        assert response.status_code == 201
        student_id = response.json()["id"]
        assert client.get(f"/api/v1/students/{student_id}").json()["name"] == "Asha"
        assert client.delete(f"/api/v1/students/{student_id}").status_code == 204


def test_validation_and_authentication() -> None:
    with TestClient(app) as client:
        assert client.post("/api/v1/students", json={"name": "", "roll_no": "1", "class_name": "CSE"}).status_code == 422
        client.post("/api/v1/teachers", json={"name": "Dr X", "email": "x@example.com", "password_hash": hash_password("secret")})
        token = client.post("/api/v1/auth/token", json={"email": "x@example.com", "password": "secret"})
        assert token.status_code == 200 and token.json()["token_type"] == "bearer"


def test_recognition_and_debouncing() -> None:
    assert FaceRecognizer().match([1, 0], {"student-1": [1, 0]}) == ("student-1", 1.0)
    debouncer = AttendanceDebouncer(30)
    assert debouncer.should_record("session", "student", now=0)
    assert not debouncer.should_record("session", "student", now=1)
    assert debouncer.should_record("session", "student", now=31)