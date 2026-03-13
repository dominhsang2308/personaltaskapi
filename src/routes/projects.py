import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.db import User, Project
from src.user import current_active_user
from src.crud import project as crud_project
from src.schemas import ProjectCreate
router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=Project, status_code=201)
async def create_project(project: ProjectCreate, current_user: User = Depends(current_active_user)):
    return await crud_project.create_project(name=project.name, description=project.description, user_id=current_user.id)

@router.get("/", response_model=list[Project])
async def read_projects(current_user: User = Depends(current_active_user)):
    return await crud_project.get_projects(user_id=current_user.id)

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: uuid.UUID, current_user: User = Depends(current_active_user)):
    project = await crud_project.get_project_by_id(project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{project_id}", response_model=Project)
async def update_project(project_id: uuid.UUID, project_update: ProjectCreate, current_user: User = Depends(current_active_user)):
    updated_project = await crud_project.update_project(
        project_id=project_id, 
        name=project_update.name, 
        description=project_update.description, 
        user_id=current_user.id
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@router.delete("/{project_id}")
async def delete_project(project_id: uuid.UUID, current_user: User = Depends(current_active_user)):
    success = await crud_project.delete_project(project_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
