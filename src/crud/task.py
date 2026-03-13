import uuid
import json
from datetime import datetime
from typing import List, Optional
from src.db import Task, Project
from src.schemas import CreateTask
from src.redis_util import redis_client

async def get_tasks(
    user_id: uuid.UUID, 
    status: Optional[str] = None, 
    project_id: Optional[uuid.UUID] = None,
    sort_by: str = "created_at",
    page: int = 1,
    limit: int = 10
) -> List[Task]:
    query = Task.find(Task.user_id == user_id)
    if status:
        query = query.find(Task.status == status)
    if project_id:
        query = query.find(Task.project.id == project_id)
    
    # Sorting and Pagination
    skip = (page - 1) * limit
    return await query.sort(sort_by).skip(skip).limit(limit).to_list()

async def get_task_by_id(task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    # Redis Cache-aside Pattern
    cache_key = f"task:{task_id}"
    cached_task = await redis_client.get(cache_key)
    if cached_task:
        return Task.model_validate_json(cached_task)

    task = await Task.find_one(Task.id == task_id, Task.user_id == user_id, fetch_links=True)
    if task:
        # Cache for 60 seconds
        await redis_client.setex(cache_key, 60, task.model_dump_json())
    return task

async def create_task(task: CreateTask, user_id: uuid.UUID) -> Task:
    new_task = Task(
        title=task.title, 
        description=task.description, 
        user_id=user_id,
        status="todo"
    )
    await new_task.insert()
    
    # Redis Pub/Sub Event System
    event = {
        "event": "task.created",
        "task_id": str(new_task.id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat()
    }
    await redis_client.publish("task_events", json.dumps(event))
    
    return new_task

async def update_task(task_id: uuid.UUID, task_update: CreateTask, user_id: uuid.UUID) -> Optional[Task]:
    existing_task = await get_task_by_id(task_id, user_id)
    if not existing_task:
        return None
        
    existing_task.title = task_update.title
    existing_task.description = task_update.description
    existing_task.updated_at = datetime.utcnow()
    
    await existing_task.save()
    
    # Invalidate Cache
    await redis_client.delete(f"task:{task_id}")
    
    return existing_task

async def delete_task(task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    task = await Task.find_one(Task.id == task_id, Task.user_id == user_id)
    if task:
        await task.delete()
        await redis_client.delete(f"task:{task_id}")
        return True
    return False

async def get_task_stats(user_id: uuid.UUID):
    pipeline = [
        {"$match": {"user_id": str(user_id)}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    return await Task.aggregate(pipeline).to_list()

# Example: Simple Event Consumer
async def task_event_consumer():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("task_events")
    async for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Received Event: {message['data']}")
