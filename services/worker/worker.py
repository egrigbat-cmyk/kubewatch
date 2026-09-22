from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@celery_app.task
def process_task(message):
    print(f"Processing task: {message}")
    return f"Processed: {message}"
