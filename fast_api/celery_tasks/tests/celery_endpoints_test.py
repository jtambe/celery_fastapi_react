import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from fast_api.celery_tasks.celery_endpoints import router
from sqlalchemy import select
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.mark.asyncio
@patch("fast_api.celery_tasks.celery_endpoints.celery_client.send_task")
@patch("fast_api.celery_tasks.celery_endpoints.redis_client.sadd", new_callable=AsyncMock)
async def test_process_task(mock_sadd, mock_send_task, app):
    mock_send_task.return_value = MagicMock(id="task123")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/api/v0/process", json={"numberA": 1, "numberB": 2})
    assert resp.status_code == 200
    assert resp.json()["status"] == "Message received and queued for processing"

@pytest.mark.asyncio
@patch("fast_api.celery_tasks.celery_endpoints.celery_rabbitmq_client.send_task")
async def test_process2_task(mock_send_task, app):
    mock_send_task.return_value = MagicMock(id="task456")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/api/v0/process2", json={"numberA": 1, "numberB": 2})
    assert resp.status_code == 200
    assert resp.json()["status"] == "Message received and queued for processing"
    assert resp.json()["task_id"] == "task456"

@pytest.mark.asyncio
@patch("fast_api.celery_tasks.celery_endpoints.redis_client.sismember", new_callable=AsyncMock)
@patch("fast_api.celery_tasks.celery_endpoints.AsyncResult")
async def test_get_task_status(mock_async_result, mock_sismember, app):
    mock_sismember.return_value = True
    mock_result = MagicMock(status="SUCCESS", ready=lambda: True, result=42)
    mock_async_result.return_value = mock_result
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v0/task_status", params={"task_id": "task123"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "SUCCESS"
    assert resp.json()["result"] == 42

@pytest.mark.asyncio
@patch("fast_api.celery_tasks.celery_endpoints.redis_client.sismember", new_callable=AsyncMock)
@patch("fast_api.celery_tasks.celery_endpoints.AsyncResult")
async def test_get_task_result(mock_async_result, mock_sismember, app):
    mock_sismember.return_value = False
    mock_result = MagicMock(status="PENDING", ready=lambda: False, result=None)
    mock_async_result.return_value = mock_result
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v0/task_result", params={"task_id": "task456"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "PENDING"
    assert resp.json()["result"] is None