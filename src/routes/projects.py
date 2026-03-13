import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.db import User, Project
from src.user import current_active_user
from src.crud import project as crud_project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=Project, status_code=201)
async def create_project(name: str, description: Optional[str] = None, current_user: User = Depends(current_active_user)):
    return await crud_project.create_project(name=name, description=description, user_id=current_user.id)

@router.get("/", response_model=list[Project])
async def read_projects(current_user: User = Depends(current_active_user)):
    return await crud_project.get_projects(user_id=current_user.id)
