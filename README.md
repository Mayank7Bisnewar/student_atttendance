# Smart Attendance Backend

FastAPI backend for student attendance with async MongoDB support, mock-safe CV services, CRUD APIs, and WebSockets.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`. MongoDB is optional for local demo mode; if the configured server is unavailable, the API uses an in-memory store. Set `CV_MODE` and provide camera/model integrations before production use.

REST resources are available under `/api/v1/students`, `/teachers`, `/classes`, `/cameras`, `/sessions`, `/attendance`, and `/logs`. Realtime endpoints are `/ws/stream/{camera_id}` and `/ws/live-attendance`.

Run checks with `pytest`.
