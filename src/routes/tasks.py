import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from src.schemas import CreateTask, TaskResponse
from src.db import Task, User
from src.user import current_active_user
from src.crud import task as crud_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: CreateTask, current_user: User = Depends(current_active_user)):
    try:
        new_task = await crud_task.create_task(task=task, user_id=current_user.id)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    status: Optional[str] = None,
    project_id: Optional[uuid.UUID] = None,
    sort_by: str = "created_at",
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(current_active_user)
):
    tasks = await crud_task.get_tasks(
        user_id=current_user.id, 
        status=status, 
        project_id=project_id,
        sort_by=sort_by,
        page=page,
        limit=limit
    )
    return tasks

@router.get("/stats")
async def get_task_stats(current_user: User = Depends(current_active_user)):
    return await crud_task.get_task_stats(user_id=current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: uuid.UUID, current_user: User = Depends(current_active_user)):
    task = await crud_task.get_task_by_id(task_id=task_id, user_id=current_user.id)
    if not task:
         raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task_by_id(task_id: uuid.UUID, current_user: User = Depends(current_active_user)):
    success = await crud_task.delete_task(task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"Message": "Task deleted successfully" }

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_by_id(task_id: uuid.UUID, task: CreateTask, current_user: User = Depends(current_active_user)):
    updated_task = await crud_task.update_task(task_id=task_id, task_update=task, user_id=current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task