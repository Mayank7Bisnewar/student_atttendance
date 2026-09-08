from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except ImportError:  # Optional during mock/demo mode.
    AsyncIOMotorClient = None  # type: ignore[assignment,misc]

from app.core.config import Settings


class MemoryCollection:
    def __init__(self) -> None:
        self.documents: dict[str, dict[str, Any]] = {}


class Database:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: Any = None
        self.database: Any = None
        self.memory: dict[str, MemoryCollection] = {}

    async def connect(self) -> None:
        if AsyncIOMotorClient is None:
            return
        self.client = AsyncIOMotorClient(self.settings.mongodb_url, serverSelectionTimeoutMS=500)
        self.database = self.client[self.settings.db_name]
        try:
            await self.client.admin.command("ping")
        except Exception:
            self.client.close()
            self.client = None
            self.database = None

    async def close(self) -> None:
        if self.client is not None:
            self.client.close()
            self.client = None
            self.database = None

    def collection(self, name: str) -> Any:
        if self.database is not None:
            return self.database[name]
        return self.memory.setdefault(name, MemoryCollection())


@asynccontextmanager
async def lifespan_database(settings: Settings) -> AsyncIterator[Database]:
    database = Database(settings)
    await database.connect()
    try:
        yield database
    finally:
        await database.close()