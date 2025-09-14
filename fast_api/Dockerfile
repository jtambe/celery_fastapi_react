FROM python:3.13-slim

WORKDIR /app

# Install uv and project dependencies
RUN pip install uv
COPY . .
RUN uv pip install --system .

EXPOSE 5000

CMD ["uvicorn", "fast_api.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--log-level", "info"]