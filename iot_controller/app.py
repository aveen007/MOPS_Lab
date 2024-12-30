from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr, ValidationError
from db import IoTData, db
from rmq import device_channels,rmq_connection,create_channel_for_device

app = FastAPI()


@app.post("/data")
async def receive_data(request: Request):
    try:
        # Parse and validate incoming data
        data = await request.json()
        # print(data)
        validated_data = IoTData(**data)

        if validated_data.device_id not in device_channels:
            print("new device connected...")
            rabbitmq_channel = create_channel_for_device(rmq_connection, validated_data.device_id)
        else:
            print("sending packets through the existing channel...")
            rabbitmq_channel = device_channels[validated_data.device_id]
        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='validated_queue',
            body=validated_data
        )

        # Save to MongoDB
        result = await db.data.insert_one(validated_data.dict())
        
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ValidationError as e:
        raise HTTPException(501, "please provide a correct name and email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Run using `uvicorn` or `hypercorn` for async support
# Example: `uvicorn main:app --host 0.0.0.0 --port 5000`


