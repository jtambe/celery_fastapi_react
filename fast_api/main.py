from fastapi import FastAPI, Request
import uvicorn

from Celery.celery_task import process, process2

app = FastAPI()


@app.post("/api/v0/process")
async def telegram_webhook(request: Request):
    numbers = await request.json()
    numberA = numbers.get("numberA")
    numberB = numbers.get("numberB")
    process.delay(numberA, numberB)
    return {"status": "Message received and queued for processing"}

@app.post("/api/v0/process2")
async def telegram_webhook(request: Request):
    numbers = await request.json()
    numberA = numbers.get("numberA")
    numberB = numbers.get("numberB")
    process2.delay(numberA, numberB)
    return {"status": "Message received and queued for processing"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)