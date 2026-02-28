from pydantic import BaseModel

class Tasks(BaseModel):
    task: str
    done: bool