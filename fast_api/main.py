from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
import redis.asyncio as aioredis
import logging
from celery_tasks.celery_endpoints import router as celery_tasks_router
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres:5432/mydb"
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     # Optionally test connection
#     async with engine.begin() as conn:
#         await conn.run_sync(lambda x: None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()
app.include_router(celery_tasks_router)