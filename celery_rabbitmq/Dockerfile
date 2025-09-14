FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

RUN pip install uv
COPY pyproject.toml .
COPY . /app
RUN uv pip install --system .


CMD ["python", "-m", "celery", "-A", "celery_rabbitmq_task", "worker", "-Q", "rabbitmq_queue", "--loglevel=info"]