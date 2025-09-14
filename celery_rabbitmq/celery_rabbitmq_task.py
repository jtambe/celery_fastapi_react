import os
from dotenv import load_dotenv
from celery import Celery
from time import sleep
from celery.result import AsyncResult
# celery -A celery_rabbitmq.celery_rabbitmq_task worker -l info

# app = celery(main="tasks", broker="pyamqp://guest:guest@localhost//", backend="rpc://")
# http://localhost:15672/#/
app = Celery(main="tasks", broker="pyamqp://", backend="rpc://")

# @app.task
# def process(x, y):
#     i = 0
#     while i < 5:
#         sleep(10)
#         i += 1
#         print("Processing...")
#
#     return x**2 + y**2

@app.task
def process2(x, y):
    i = 0
    while i < 5:
        sleep(1)
        i += 1
        print("Processing through rabbitmq...")
    return x + y


def get_task_result(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return result.result
    else:
        return f"Task {task_id} is not ready. Status: {result.status}"

def get_task_status(task_id):
    result = AsyncResult(task_id)
    return result.status
