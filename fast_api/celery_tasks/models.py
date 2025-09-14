from pydantic import BaseModel
from typing import Optional

class Numbers(BaseModel):
    numberA: int
    numberB: int

class Task(BaseModel):
    task_id: str
    status: Optional[str] = None
    result: Optional[int] = None