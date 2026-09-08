from datetime import datetime
from typing import Any, TypeVar

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from app.models.common import (
    Attendance, AttendanceCreate, Camera, CameraCreate, Course, CourseCreate,
    Log, LogCreate, Session, SessionCreate, Student, StudentCreate, Teacher,
    TeacherCreate,
)

router = APIRouter(prefix="/api/v1")
ModelT = TypeVar("ModelT", bound=BaseModel)


def _store(request: Request, collection: str) -> dict[str, dict[str, Any]]:
    return request.app.state.database.collection(collection).documents


def _create(request: Request, collection: str, payload: ModelT) -> ModelT:
    data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    _store(request, collection)[data["id"]] = data
    return payload


def _list(request: Request, collection: str, model: type[ModelT]) -> list[ModelT]:
    return [model(**item) for item in _store(request, collection).values()]


def _get(request: Request, collection: str, item_id: str, model: type[ModelT]) -> ModelT:
    item = _store(request, collection).get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return model(**item)


def _delete(request: Request, collection: str, item_id: str) -> None:
    if _store(request, collection).pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Resource not found")


def _update(request: Request, collection: str, item_id: str, payload: BaseModel, model: type[ModelT]) -> ModelT:
    current = _get(request, collection, item_id, model)
    updates = payload.model_dump(exclude_unset=True) if hasattr(payload, "model_dump") else payload.dict(exclude_unset=True)
    data = current.model_dump() if hasattr(current, "model_dump") else current.dict()
    data.update(updates)
    data["updated_at"] = datetime.utcnow()
    _store(request, collection)[item_id] = data
    return model(**data)


def register_crud(path: str, collection: str, model: type[ModelT], create_model: type[BaseModel]) -> None:
    @router.post(path, response_model=model, status_code=status.HTTP_201_CREATED)
    async def create(request: Request, payload: create_model) -> ModelT:  # type: ignore[valid-type]
        return _create(request, collection, model(**(payload.model_dump() if hasattr(payload, "model_dump") else payload.dict())))

    @router.get(path, response_model=list[model])  # type: ignore[valid-type]
    async def list_items(request: Request) -> list[ModelT]:
        return _list(request, collection, model)

    @router.get(f"{path}/{{item_id}}", response_model=model)
    async def get_item(request: Request, item_id: str) -> ModelT:
        return _get(request, collection, item_id, model)

    @router.put(f"{path}/{{item_id}}", response_model=model)
    async def update(request: Request, item_id: str, payload: create_model) -> ModelT:  # type: ignore[valid-type]
        return _update(request, collection, item_id, payload, model)

    @router.delete(f"{path}/{{item_id}}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(request: Request, item_id: str) -> None:
        _delete(request, collection, item_id)


register_crud("/students", "students", Student, StudentCreate)
register_crud("/teachers", "teachers", Teacher, TeacherCreate)
register_crud("/classes", "classes", Course, CourseCreate)
register_crud("/cameras", "cameras", Camera, CameraCreate)
register_crud("/sessions", "sessions", Session, SessionCreate)
register_crud("/attendance", "attendance", Attendance, AttendanceCreate)
register_crud("/logs", "logs", Log, LogCreate)