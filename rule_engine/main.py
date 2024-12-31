import asyncio
from rmq import connect
from prometheus_client import start_http_server


async def main():
    start_http_server(8080)
    connection, channel = await connect()
    try:
        await asyncio.Future()
    finally:
        await channel.close()
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
