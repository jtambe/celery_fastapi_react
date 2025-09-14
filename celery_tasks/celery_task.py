import os
from dotenv import load_dotenv
from celery import Celery
from time import sleep
from celery.result import AsyncResult
# celery -A celery_tasks.celery_task worker -l info

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
broker_url = os.getenv("CELERY_BROKER_URL")
backend_url = os.getenv("CELERY_RESULT_BACKEND")

app = Celery("tasks", broker=broker_url, backend=backend_url)
# app = Celery("tasks", broker="redis://redis:6379", backend="redis://redis:6379")# http://127.0.0.1:8081/

@app.task
def process(x, y):
    try:
        i = 0
        while i < 5:
            sleep(3)
            i += 1
            print("Processing through Redis broker...")
        print(f"Processing x={x}, y={y}")
        if x == -1:  # Simulate failure for a specific input
            raise ValueError("Simulated task failure")
        return x**2 + y**2
    except Exception as e:
        print(f"Error occurred: {e}")
        raise e

def get_task_result(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return result.result
    else:
        return f"Task {task_id} is not ready. Status: {result.status}"

def get_task_status(task_id):
    result = AsyncResult(task_id)
    return result.status
