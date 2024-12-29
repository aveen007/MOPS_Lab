from fastapi import FastAPI, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, ValidationError

app = FastAPI()

# MongoDB setup
mongo_client = AsyncIOMotorClient("mongodb://mongo:27017")
db = mongo_client.iot_db  # Specify the database

# Data model for validation
class IoTData(BaseModel):
    device_id: str
    name: str
    email: EmailStr
    age: int
    x_factor: float

@app.post("/data")
async def receive_data(request: Request):
    try:
        # Parse and validate incoming data
        data = await request.json()
        print(data)
        validated_data = IoTData(**data)

        # Save to MongoDB
        result = await db.data.insert_one(validated_data.dict())
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run using `uvicorn` or `hypercorn` for async support
# Example: `uvicorn main:app --host 0.0.0.0 --port 5000`

# import pika
# RabbitMQ setup
# rabbitmq_host = 'rabbitmq'
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
# channel = connection.channel()
# channel.queue_declare(queue='rules_queue')
