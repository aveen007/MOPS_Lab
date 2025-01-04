import aiohttp
import requests
import random
import time
import asyncio
import random
import string
import os
import logging
from promethuous import REQUESTS_TOTAL,REQUESTS_DURATION
import time
from prometheus_client import start_http_server

logging.basicConfig(
    filename='/var/log/data_simulator.log',
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',  
    filemode='a'
)

def generate_data():
    first_names = ["John", "Jane", "Alex", "Emily", "Chris"]
    last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis"]
    domains = ["yandex.com", "google.com", "hotmail.com"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

    return {
        "device_id": f"device_{random.randint(1, 5)}",
        "name": f"{first_name} {last_name}",
        "email": email,
        "age": random.randint(18, 80),
        "x_factor": round(random.uniform(0.1, 10.0), 2)
    }

# Example usage:
data = generate_data()
# print(data)
import random
import string

def generate_data():
    first_names = ["John", "Jane", "Alex", "Emily", "Chris"]
    last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis"]
    domains = ["example.com", "test.com", "demo.com"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

    return {
        "device_id": f"device_{random.randint(1, 5)}",
        "name": f"{first_name} {last_name}",
        "email": email,
        "age": random.randint(18, 80),
        "x_factor": round(random.uniform(0.1, 50.0), 2)
    }

async def send_data(session, url):
    while True:
        data = generate_data()
        try:
            start=time.time()
            async with session.post(url, json=data) as response:
                logging.info(f"Sent data , Response: {response.status}")
                REQUESTS_TOTAL.labels(status="success").inc()
            end=time.time()
            REQUESTS_DURATION.observe(end-start)
        except Exception as e:
            logging.error(f"Error sending data: {e}")
        await asyncio.sleep(2)  # Send data every 2 seconds

async def main():
    start_http_server(8070)
    url = "http://iot_controller:5000/data"
    async with aiohttp.ClientSession() as session:
        await send_data(session, url)

# Run the asynchronous simulation
asyncio.run(main())