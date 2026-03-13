import uuid
from typing import List, Optional
from src.db import Project

async def get_projects(user_id: uuid.UUID) -> List[Project]:
    return await Project.find(Project.user_id == user_id).to_list()

async def create_project(name: str, description: Optional[str], user_id: uuid.UUID) -> Project:
    new_project = Project(name=name, description=description, user_id=user_id)
    await new_project.insert()
    return new_project

async def get_project_by_id(project_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Project]:
    return await Project.find_one(Project.id == project_id, Project.user_id == user_id)
