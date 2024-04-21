from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from tasks import tasks



app = FastAPI()

class Task(BaseModel):
    title: str
    description: str = ""
    done: bool = False

@app.get("/todo/api/v1.0/tasks")
async def get_tasks():

    return {'tasks': tasks}

@app.get("/todo/api/v1.0/tasks/{task_id}")
async def get_task(task_id: int):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {'task': task[0]}

@app.post("/todo/api/v1.0/tasks", status_code=201)
def create_task(task:Task):
    if not task.title:
        raise HTTPException(status_code=400, detail="Title is required")
    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': task.title,
        'description': task.description,
        'done': task.done
    }
    tasks.append(new_task)
    return {"task": new_task}

@app.middleware("http")
async def validate_content_type(request, call_next):
    if request.method == 'POST':
        if "application/json" not in request.headers.get("content-type", ""):
            raise HTTPException(status_code=415, detail="Unsupported Media Type. Content-Type header must be application/json.")
    
    response = await call_next(request)
    return response

# @app.get("/")
# async def root():
#     return {"message": "Y'all are not ready!!!"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id} 

# success - 2xx
# client errors - 4xx
# server errors - 5xx