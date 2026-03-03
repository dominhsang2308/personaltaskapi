import uuid

from fastapi import Depends, FastAPI, HTTPException
from .schemas import CreateTask, TaskResponse, UserCreate, UserRead, UserUpdate
from .db import Task, get_session, create_db_and_tables, get_db, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select, delete

from src.user import current_activate_user, auth_backend, fastapi_users

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])

@app.post("/tasks/", response_model=TaskResponse, status_code=201)
async def create_task(task:CreateTask, db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    new_task = Task(title = task.title, description = task.description, user_id = current_user.id)
    try:
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/tasks/", response_model = list[TaskResponse])
async def read_tasks(db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    tasks = result.scalars().all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id:uuid.UUID,db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user == current_user.id))
    tasks = result.scalars().first()
    return tasks

@app.delete('/delete_task/{task_id}')
async def delete_task_by_id(task_id:uuid.UUID, db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    result = await db.execute(delete(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not found")
    await db.commit()
    return {"Message":"Task delete sucessfully" }


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_by_id(task_id:uuid.UUID, db:AsyncSession = Depends(get_db), task:CreateTask = None):
    results = await db.execute(select(Task).where(Task.id == task_id))
    existing_task = results.scalars().first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Not found")
    existing_task.title = task.title
    existing_task.description = task.description
    await db.commit()
    await db.refresh(existing_task)
    return existing_task
    

