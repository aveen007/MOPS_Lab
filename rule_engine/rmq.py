import aiormq, asyncio
import time
import pika
from db import IoTData, instant,ongoing,db
import json
from promethuous import INSTANT_RULES_COUNTER,ONGOING_RULES_COUNTER
rabbitmq_host = 'rabbitmq'


# Establish connection to RabbitMQ
async def connect():
    try:
        connection = await aiormq.connect("amqp://rabbitmq:5672/")

        channel =await connection.channel(publisher_confirms=False)
        await channel.basic_consume('validated_queue', callback)
        return connection, channel
        # Acknowledge the message
        # ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error in message handling: {e}")
        await asyncio.sleep(2)
        # Optionally, reject the message without requeueing
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

async def parse_message(message_body:bytes):
    """
    Process the message body, validating it as IoTData.
    """
    try:
        # Decode the message body from bytes to a string
        message_data = json.loads(message_body.decode("utf-8"))

        # Validate the data using IoTData schema
        iot_data = IoTData(**message_data)
        print(f"Received IoTData: {iot_data}")
        # if (iot_data.device_id==42):
        if iot_data.x_factor <= 5:
            INSTANT_RULES_COUNTER.inc()
            await instant.insert_one({
                "device_id": iot_data.device_id,
                "alpha": iot_data.x_factor,
            })

        current_id_stack = ongoing[f"{iot_data.device_id}_stack"]
        await current_id_stack.insert_one(message_data)

        pipeline = [
            {"$match": {"device_id": iot_data.device_id, "age": {"$gte": 42}}},
            {"$count": "total_count"}
        ]
        result = await current_id_stack.aggregate(pipeline).to_list(length=None)

        if result:
            total_count = result[0]['total_count']
            if total_count >= 5:
                ONGOING_RULES_COUNTER.inc()
                await ongoing.insert_one({
                    "device_id": iot_data.device_id,
                    "timestamp": str(time.time())
                })

                await db.drop_collection(current_id_stack)


            if await current_id_stack.count_documents({}) >= 10:
                await db.drop_collection(current_id_stack)

        # await message.channel.basic_ack(message.delivery_tag)

        # TODO
        # Save to a database, trigger other actions, etc.

   
    except json.JSONDecodeError as e:
       print(f"JSON decoding error: {e}")
    except Exception as e:
       print(f"Unexpected error: {e}")


# Set up the consumer
async def callback( message: aiormq.abc.DeliveredMessage):
    try:
        await parse_message(message.body)
    except Exception as e:
        await message.channel.basic_nack(message.delivery_tag)