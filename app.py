from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from tasks import tasks



app = FastAPI()

class Task(BaseModel):
    title: str
    description: str = ""
    done: bool = False

def make_public_task(task: dict, request:Request):
    new_task = {}
    for field, value in task.items():
        if field == "id":
            url = str(request.url).rstrip('/')
            new_task['uri'] = f"{url}/{task['id']}"
        else:
            new_task[field] = value
    return new_task

@app.get("/todo/api/v1.0/tasks")
async def get_tasks(request: Request):

    return {'tasks': [make_public_task(task, request) for task in tasks]}

@app.get("/todo/api/v1.0/tasks/{task_id}")
async def get_task(task_id: int, request:Request):
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

@app.put("/todo/api/v1.0/tasks/{task_id}")
async def update_task(task_id: int, task_data: Task):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    task[0]['title'] = task_data.title
    task[0]['description'] = task_data.description
    task[0]['done'] = task_data.done

    return {"task" : task}

@app.delete("/todo/api/v1.0/tasks/{task_id}")
async def delete_task(task_id: int):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks.remove(task[0])
    return {"result": True}

@app.middleware("http")
async def validate_content_type(request, call_next):
    if request.method == 'POST':
        if "application/json" not in request.headers.get("content-type", ""):
            raise HTTPException(status_code=415, detail="Unsupported Media Type. Content-Type header must be application/json.")
    
    response = await call_next(request)
    return response