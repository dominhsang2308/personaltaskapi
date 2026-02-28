from fastapi import FastAPI, HTTPException
from .schemas import Tasks
from .db import Task, get_session, create_db_and_tables
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


personal_task = {
    1: {"task": "Buy groceries", "done": False},
    2: {"task": "Walk the dog", "done": True}
}

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/tasks")
def get_task():
    return personal_task

@app.get("/tasks/{id}")
def get_task_by_id(id:int):
    if id not in personal_task:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return personal_task.get(id)

@app.post("/create_tasks")
def create_task(tasks:Tasks):
    new_post = {"task": tasks.task, "done": tasks.done}
    personal_task[max(personal_task.keys()) +1] = new_post
    return new_post