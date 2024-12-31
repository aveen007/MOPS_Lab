import aiormq, asyncio
import time
import pika
from db import IoTData
import json
rabbitmq_host = 'rabbitmq'


# Establish connection to RabbitMQ
async def connect():
    try:
        print("hi")
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

        # TODO
        # Save to a database, trigger other actions, etc.

   
    except json.JSONDecodeError as e:
       print(f"JSON decoding error: {e}")
    except Exception as e:
       print(f"Unexpected error: {e}")


# Set up the consumer
async def callback( message: aiormq.abc.DeliveredMessage):
    try:
        print("Yaoza")
        await parse_message(message.body)
    except Exception as e:
        await message.channel.basic_nack(message.delivery_tag)
