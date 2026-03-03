from datetime import datetime
from typing import Optional
import uuid

from fastapi_users import schemas

from pydantic import BaseModel, Field
from pygments.lexer import default

class CreateTask(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):  # hoặc TaskOut, TaskCreate nếu bạn dùng
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)   # ← đúng cách
    updated_at: datetime = Field(default_factory=datetime.utcnow)   # ← đúng cách

    class Config:  # hoặc model_config ở v2.5+
        from_attributes = True  # nếu trả về từ ORM


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUser[uuid.UUID]):
    pass