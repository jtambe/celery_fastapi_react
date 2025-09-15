from celery import Celery
import redis.asyncio as aioredis
from .models import Numbers
import os
from .schema import CeleryTaskMeta
from fastapi import APIRouter, Query
from celery.result import AsyncResult
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
import pickle
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from fast_api.database import get_db

logger = logging.getLogger(__name__)

redis_broker_url = os.getenv("CELERY_REDIS_BROKER_URL")
redis_backend_url = os.getenv("CELERY_REDIS_RESULT_BACKEND")
celery_client = Celery(broker=redis_broker_url, backend=redis_backend_url)

rabbitmq_broker_url = os.getenv("CELERY_RABBITMQ_BROKER_URL")
rabbitmq_backend_url = os.getenv("CELERY_RABBITMQ_RESULT_BACKEND")
celery_rabbitmq_client = Celery(broker=rabbitmq_broker_url,backend=rabbitmq_backend_url)

# import redis ## only sync version not async
# redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
redis_client = aioredis.Redis(host="redis",port=6379,decode_responses=True)
TASK_SET_KEY = "celery_task_id"

router = APIRouter()

@router.post("/api/v0/process")
async def process_task(numbers: Numbers):
    try:
        task = celery_client.send_task("celery_task.process", args=[numbers.numberA, numbers.numberB])
        await redis_client.sadd(TASK_SET_KEY, task.id)
        return {"status": "Message received and queued for processing"}
    except Exception as e:
        logger.error(f"Error in process_task: {e}")
        return {"status": "Error", "message": "something went wrong"}

'''
{
  "numberA": 4,
  "numberB": 2
}
'''
@router.post("/api/v0/process2")
async def process2_task(numbers: Numbers):
    try:
        task = celery_rabbitmq_client.send_task(
            "celery_rabbitmq_task.process2",
            args=[numbers.numberA, numbers.numberB],
            queue="rabbitmq_queue"
        )
        return {"status": "Message received and queued for processing", "task_id": task.id}
    except Exception as e:
        logger.error(f"Error in process2_task: {e}")
        return {"status": "Error", "message": "something went wrong"}


@router.get("/api/v0/task_status")
async def get_task_status(task_id: str = Query(...)):
    try:
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
    except Exception as e:
        logger.error(f"Error in get_task_status: {e}")
        return {"status": "Error", "message": "something went wrong"}

@router.get("/api/v0/task_result")
async def get_task_result(task_id: str = Query(...)):
    try:
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
    except Exception as e:
        logger.error(f"Error in get_task_result: {e}")
        return {"status": "Error", "message": "something went wrong"}

def _safe_result(result):
    if isinstance(result, (str, int, float, bool)):
        return result
    return ""

@router.get("/api/v0/all_tasks")
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    try:
        task_ids = await redis_client.smembers(TASK_SET_KEY)
        pg_sql_db_result = await db.execute(select(CeleryTaskMeta))
        rabbitmq_tasks = pg_sql_db_result.scalars().all()
        print(rabbitmq_tasks)
        tasks = []
        for task_id in task_ids:
            result = AsyncResult(task_id, app=celery_client)
            tasks.append({
                "task_id": task_id,
                "status": result.status,
                "result": _safe_result(result.result) if result.ready() else ""
            })
        for t in rabbitmq_tasks:
            raw_result = pickle.loads(t.result) if t.result else ""
            tasks.append({
                "task_id": t.task_id,
                "status": t.status,
                "result": _safe_result(raw_result),
            })
        return tasks
    except Exception as e:
        logger.error(f"Error in get_all_tasks: {e}")
        return {"status": "Error", "message": "something went wrong in get_all_tasks"}