from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date

class TaskBase(SQLModel):
    name: str = Field(description="The name of the task")
    description: str = Field(description="Detailed description of the task")
    due_date: date = Field(description="The due date of the task")
    priority: int = Field(description="The priority of the task from 1 (high priority) to 5 (low priority)")
    status: str = Field(description="The status of the task. Can be 'Not Started', 'In Progress', 'Completed', or 'Cancelled'")
    expected_time_hours: float = Field(description="The expected time to complete the task in hours")

class Task(TaskBase, table=True):
    task_id: Optional[int] = Field(default=None, primary_key=True, description="The ID of the task")

class TaskCreate(TaskBase):
    "Create a new task"
    pass

class TaskUpdate(TaskBase):
    "Update an existing task"
    task_id: int = Field(description="The ID of the task")

class TaskRead(TaskBase):
    task_id: int = Field(description="The ID of the task")