import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.schemas import CreateTask, TaskResponse
from src.db import Task, get_db, User
from src.user import current_activate_user
from src.crud import task as crud_task

#Creating router. 
router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task:CreateTask, db:AsyncSession = Depends(get_db), current_user: User = Depends(current_activate_user)):
    try:
        new_task = await crud_task.create_task(db=db, task=task, user_id=current_user.id)
        return new_task
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[TaskResponse])
async def read_tasks(db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    tasks = await crud_task.get_tasks(db=db, user_id=current_user.id)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id:uuid.UUID, db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    task = await crud_task.get_task_by_id(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
         raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task_by_id(task_id:uuid.UUID, db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)):
    success = await crud_task.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"Message": "Task deleted successfully" }

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_by_id(task_id:uuid.UUID, task:CreateTask, db:AsyncSession = Depends(get_db), current_user:User = Depends(current_activate_user)): # Fixed task argument order
    updated_task = await crud_task.update_task(db=db, task_id=task_id, task_update=task, user_id=current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task