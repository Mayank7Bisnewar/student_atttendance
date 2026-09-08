from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.core.security import create_access_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1)


@router.post("/token")
async def login(request: Request, payload: LoginRequest) -> dict[str, str]:
    teachers = request.app.state.database.collection("teachers").documents.values()
    teacher = next((item for item in teachers if item.get("email") == payload.email), None)
    if teacher is None or not verify_password(payload.password, teacher["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(teacher["id"]), "token_type": "bearer"}