import uuid

from fastapi import Depends, FastAPI, HTTPException
from .schemas import CreateTask, TaskResponse
from .db import Task, get_session, create_db_and_tables, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select, delete

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/tasks/", response_model=TaskResponse, status_code=201)
async def create_task(task:CreateTask, db:AsyncSession = Depends(get_db)):
    new_task = Task(title = task.title, description = task.description)
    try:
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/tasks/", response_model = list[TaskResponse])
async def read_tasks(db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id:uuid.UUID,db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    tasks = result.scalars().first()
    return tasks

@app.delete('/delete_task/{task_id}')
async def delete_task_by_id(task_id:uuid.UUID, db:AsyncSession = Depends(get_db)):
    result = await db.execute(delete(Task).where(Task.id == task_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not found")
    await db.commit()
    return {"Message":"Task delete sucessfully" }
    

