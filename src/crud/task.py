import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.db import Task
from src.schemas import CreateTask

async def get_tasks(db: AsyncSession, user_id: uuid.UUID) -> list[Task]:
    result = await db.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()

async def get_task_by_id(db: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    return result.scalars().first()

async def create_task(db: AsyncSession, task: CreateTask, user_id: uuid.UUID) -> Task:
    new_task = Task(title=task.title, description=task.description, user_id=user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def update_task(db: AsyncSession, task_id: uuid.UUID, task_update: CreateTask, user_id: uuid.UUID) -> Task | None:
    # Get existing task
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    existing_task = result.scalars().first()
    
    if not existing_task:
        return None
        
    existing_task.title = task_update.title
    existing_task.description = task_update.description
    
    await db.commit()
    await db.refresh(existing_task)
    return existing_task

async def delete_task(db: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    result = await db.execute(delete(Task).where(Task.id == task_id, Task.user_id == user_id))
    await db.commit()
    return result.rowcount > 0
