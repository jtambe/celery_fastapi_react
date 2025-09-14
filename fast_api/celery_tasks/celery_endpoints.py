from celery import Celery
import redis.asyncio as aioredis
from .models import Numbers, Task
from fastapi import APIRouter, Query
from celery.result import AsyncResult
import logging

logger = logging.getLogger(__name__)
celery_client = Celery(
    broker="redis://redis:6379",
    backend="redis://redis:6379"
)
celery_rabbitmq_client = Celery(
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://"
)
# import redis ## only sync version not async
# redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
redis_client = aioredis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)
TASK_SET_KEY = "celery_task_id"
RABBITMQ_TASK_SET_KEY = "rabbitmq_task_id"

router = APIRouter()

'''
{
  "numberA": 4,
  "numberB": 2
}
'''
@router.post("/api/v0/process")
async def process_task(numbers: Numbers):
    task = celery_client.send_task("celery_task.process", args=[numbers.numberA, numbers.numberB])
    await redis_client.sadd(TASK_SET_KEY, task.id)
    return {"status": "Message received and queued for processing"}

'''
{
  "numberA": 4,
  "numberB": 2
}
'''
@router.post("/api/v0/process2")
async def process2_task(numbers: Numbers):
    task = celery_rabbitmq_client.send_task(
        "celery_rabbitmq_task.process2",
        args=[numbers.numberA, numbers.numberB],
        queue="rabbitmq_queue"
    )
    await redis_client.sadd(RABBITMQ_TASK_SET_KEY, task.id)
    return {"status": "Message received and queued for processing"}


@router.get("/api/v0/task_status")
async def get_task_status(task_id: str = Query(...)):
    exists = await redis_client.sismember(TASK_SET_KEY, task_id)
    logger.info(f"exists in redis: {exists}")
    if exists:
        result = AsyncResult(task_id, app=celery_client)
    else:
        result = AsyncResult(task_id, app=celery_rabbitmq_client)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

@router.get("/api/v0/task_result")
async def get_task_result(task_id: str = Query(...)):
    exists = await redis_client.sismember(TASK_SET_KEY, task_id)
    logger.info(f"exists in redis: {exists}")
    if exists:
        result = AsyncResult(task_id, app=celery_client)
    else:
        result = AsyncResult(task_id, app=celery_rabbitmq_client)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

@router.get("/api/v0/all_tasks")
async def get_all_tasks():
    task_ids = await redis_client.smembers(TASK_SET_KEY)
    rabbitmq_task_ids = await redis_client.smembers(RABBITMQ_TASK_SET_KEY)
    tasks = []
    for task_id in set(task_ids) | set(rabbitmq_task_ids):
        app = celery_client if task_id in task_ids else celery_rabbitmq_client
        result = AsyncResult(task_id, app=app)
        tasks.append({
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None
        })
    return tasks