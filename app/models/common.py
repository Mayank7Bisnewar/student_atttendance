from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    roll_no: str = Field(min_length=1)
    class_name: str = Field(min_length=1)
    department: str | None = None
    face_embeddings: list[list[float]] = Field(default_factory=list)
    status: str = "active"


class Student(StudentCreate, Entity):
    pass


class TeacherCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str
    password_hash: str
    subjects: list[str] = Field(default_factory=list)


class Teacher(TeacherCreate, Entity):
    pass


class CourseCreate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)
    schedule: dict[str, Any] = Field(default_factory=dict)


class Course(CourseCreate, Entity):
    pass


class CameraCreate(BaseModel):
    name: str = Field(min_length=1)
    location: str
    source: str = "0"
    status: str = "offline"


class Camera(CameraCreate, Entity):
    pass


class SessionCreate(BaseModel):
    subject_id: str
    teacher_id: str
    camera_id: str | None = None
    active: bool = True


class Session(SessionCreate, Entity):
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: datetime | None = None


class AttendanceCreate(BaseModel):
    session_id: str
    student_id: str
    status: str = "present"
    confidence: float = Field(ge=0, le=1)
    camera_id: str | None = None


class Attendance(AttendanceCreate, Entity):
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LogCreate(BaseModel):
    level: str = "info"
    event_type: str
    message: str


class Log(LogCreate, Entity):
    timestamp: datetime = Field(default_factory=datetime.utcnow)