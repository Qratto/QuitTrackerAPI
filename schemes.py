from pydantic import BaseModel
from datetime import datetime

class BadHabit(BaseModel):
    name: str
    description: str

class CreateBadHabit(BadHabit):
    pass

class ResponseBadHabit(BadHabit):
    id: int
    started_at: datetime


