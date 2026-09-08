import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/stream/{camera_id}")
async def stream(websocket: WebSocket, camera_id: str) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"camera_id": camera_id, "type": "frame", "mode": "mock"})
            await asyncio.sleep(0.1)
    except (WebSocketDisconnect, RuntimeError):
        return


@router.websocket("/ws/live-attendance")
async def live_attendance(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"type": "attendance", "status": "connected"})
            await asyncio.sleep(5)
    except (WebSocketDisconnect, RuntimeError):
        return