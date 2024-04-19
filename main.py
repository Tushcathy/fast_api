from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from tasks import tasks



app = FastAPI()

@app.get("/todo/api/v1.0/tasks")
async def get_tasks():

    return {'tasks': tasks}

@app.get("/todo/api/v1.0/tasks/{task_id}")
async def get_task(task_id: int):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {'task': task[0]}

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