from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import uvicorn

app = FastAPI()

# In-memory database
projects = []
tasks = []

class Project(BaseModel):
    id: Optional[int] = None
    name: str
    start_date: date
    end_date: date

class Task(BaseModel):
    id: Optional[int] = None
    project_id: int
    name: str
    start_date: date
    end_date: date

# Project CRUD operations
@app.post("/projects/", response_model=Project)
def create_project(project: Project):
    project.id = len(projects) + 1
    projects.append(project)
    return project

@app.get("/projects/", response_model=List[Project])
def read_projects():
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int):
    for project in projects:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, updated_project: Project):
    for i, project in enumerate(projects):
        if project.id == project_id:
            updated_project.id = project_id
            projects[i] = updated_project
            return updated_project
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for i, project in enumerate(projects):
        if project.id == project_id:
            del projects[i]
            return {"message": "Project deleted successfully"}
    raise HTTPException(status_code=404, detail="Project not found")

# Task CRUD operations
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)