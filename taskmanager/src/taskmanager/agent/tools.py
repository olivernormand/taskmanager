import requests
from pydantic import BaseModel, Field

from taskmanager.models.task import TaskCreate, TaskUpdate

BASE_URL = "http://localhost:8000"

class TaskGetAll(BaseModel):
    "Get all tasks"

def get_all_tasks(input: TaskGetAll = None) -> str:
    response = requests.get(BASE_URL + "/tasks/")
    response.raise_for_status()
    return str(response.json())

class TaskGet(BaseModel):
    "Get a task by its ID"
    task_id: int = Field(description="The ID of the task to get")

def get_task(input: TaskGet) -> str:
    response = requests.get(BASE_URL + f"/tasks/{input.task_id}")
    response.raise_for_status()
    return str(response.json())

def create_task(input: TaskCreate) -> str:
    response = requests.post(BASE_URL + "/tasks/", data=input.model_dump_json())
    response.raise_for_status()
    return str(response.json())

def update_task(input: TaskUpdate) -> str:
    response = requests.put(BASE_URL + f"/tasks/{input.task_id}", data=input.model_dump_json())
    response.raise_for_status()
    return str(response.json())

class TaskDelete(BaseModel):
    "Delete a task by its ID"
    task_id: str

def delete_task(input: TaskDelete) -> str:
    response = requests.delete(BASE_URL + f"/tasks/{input.task_id}")
    response.raise_for_status()
    return str(response.json())
    
    