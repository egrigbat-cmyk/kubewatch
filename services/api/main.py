from celery import Celery
from fastapi import FastAPI
from celery.result import AsyncResult
import time
from prometheus_client import Counter, Histogram, make_asgi_app
from starlette.requests import Request

app = FastAPI(title="Observability API")

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "API request latency in seconds",
    ["method", "endpoint"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    route = request.scope.get("route")
    endpoint = route.path if route else request.url.path

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint,
    ).observe(duration)

    return response


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

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
