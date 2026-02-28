from collections.abc import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    id = Column(UUID, primary_key=True, default=uuid.uuid4)


class Task(Base):
    __tablename__ = "tasks"
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

engine = create_async_engine(DATABASE_URL, echo=True,connect_args={"check_same_thread": False})

async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session