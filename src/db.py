from datetime import datetime
from typing import Optional, List
import uuid
from pydantic import BaseModel, Field
from beanie import Document, Indexed, Link, init_beanie
from fastapi_users_db_beanie import BeanieBaseUser, BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings

from pymongo.collation import Collation

class User(BeanieBaseUser, Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        email_collation = Collation(locale="en", strength=2)

class Comment(BaseModel):
    user_id: uuid.UUID
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Project(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: Indexed(str)
    description: Optional[str] = None
    user_id: uuid.UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "projects"

class Task(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: Indexed(str)
    description: Optional[str] = None
    status: Indexed(str) = "todo"
    user_id: uuid.UUID
    project: Optional[Link[Project]] = None
    comments: List[Comment] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tasks"
        indexes = [
            [
                ("user_id", 1),
                ("created_at", -1),
            ],
        ]

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL, uuidRepresentation="standard")
    await init_beanie(
        database=client.get_default_database(),
        document_models=[User, Task, Project]
    )

async def get_user_db():
    yield BeanieUserDatabase(User)