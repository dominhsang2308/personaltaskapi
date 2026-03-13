from datetime import datetime
from typing import Optional, List
import uuid

from fastapi_users import schemas

from pydantic import BaseModel, Field, field_validator
from beanie import Link

class CreateTask(BaseModel):
    title: str
    description: str
    project_id: Optional[uuid.UUID] = None

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CommentSchema(BaseModel):
    user_id: uuid.UUID
    content: str
    created_at: datetime

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    status: str = "todo"
    user_id: uuid.UUID
    project_id: Optional[uuid.UUID] = Field(None, alias="project")
    comments: List[CommentSchema] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("project_id", mode="before")
    @classmethod
    def serialize_link(cls, v):
        if isinstance(v, Link):
            return v.ref.id
        return v

    class Config:
        from_attributes = True
        populate_by_name = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUser[uuid.UUID]):
    pass