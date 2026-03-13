from datetime import datetime
from typing import Optional
import uuid

from fastapi_users import schemas

from pydantic import BaseModel, Field
from pygments.lexer import default

class CreateTask(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    status: str = "todo"
    user_id: uuid.UUID
    project: Optional[uuid.UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUser[uuid.UUID]):
    pass