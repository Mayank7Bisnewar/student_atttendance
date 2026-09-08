from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints.resources import router as resources_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.websockets.routes import router as websocket_router
from app.core.config import get_settings
from app.core.database import lifespan_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with lifespan_database(get_settings()) as database:
        app.state.database = database
        yield


app = FastAPI(title=get_settings().app_name, version="1.0.0", lifespan=lifespan)
app.include_router(resources_router)
app.include_router(auth_router)
app.include_router(websocket_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "mode": get_settings().cv_mode}