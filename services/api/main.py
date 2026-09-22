from celery import Celery
from fastapi import FastAPI
from celery.result import AsyncResult

app = FastAPI(title="Observability API")


@app.get("/")
def root():
    return {
        "service": "api",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/info")
def  info():
    return {
       "name": "Observability API",
       "version": "1.0.0"
    }

celery_app = Celery(
    "api",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@app.post("/tasks")
def create_task(message: str):
    task = celery_app.send_task(
        "worker.process_task",
        args=[message]
    )

    return {
        "task_id": task.id,
        "status": "submitted"
    }

@app.get("/tasks/{task_id}")
def  get_task(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status
    }
