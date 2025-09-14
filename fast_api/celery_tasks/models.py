from pydantic import BaseModel
from typing import Optional

class Numbers(BaseModel):
    numberA: int
    numberB: int

class Task(BaseModel):
    id: str
    status: Optional[str] = None