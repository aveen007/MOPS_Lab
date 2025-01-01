import json
from fastapi import FastAPI, Request, HTTPException,Response
from pydantic import BaseModel, EmailStr, ValidationError
from db import IoTData, db
from rmq import device_channels,rmq_connection,create_channel_for_device
from promethuous import REQUESTS_ACCEPTED,REQUESTS_DECLINED,REQUESTS
from prometheus_client import start_http_server,generate_latest,CONTENT_TYPE_LATEST

app = FastAPI()

@app.get("/metrics")
def metrics():
    REQUESTS.inc()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/data")
async def receive_data(request: Request):
    try:
        REQUESTS.inc()
        # Parse and validate incoming data
        data = await request.json()
        # print(data)
        validated_data = IoTData(**data)
        if (validated_data.age<21):
            REQUESTS_DECLINED.inc()
            raise HTTPException(501,"declined, age must be >= 21")
        data_bytes = json.dumps(data).encode('utf-8')
        if validated_data.device_id not in device_channels:
            REQUESTS_ACCEPTED.inc()
            print("new device connected...")
            rabbitmq_channel = create_channel_for_device(rmq_connection, validated_data.device_id)
        else:
            print("sending packets through the existing channel...")
            rabbitmq_channel = device_channels[validated_data.device_id]
        print(rabbitmq_channel)
        
        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='validated_queue',
            body=data_bytes
        )


        # Save to MongoDB
        result = await db.data.insert_one(validated_data.dict())
        print("Message sent")

        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ValidationError as e:
        raise HTTPException(501, "please provide a correct name and email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


