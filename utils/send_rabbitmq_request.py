from aio_pika import Message, connect
import os
import uuid
import asyncio
import json
from machine_data_model.protocols.frost_v1.frost_message import FrostMessage
from aio_pika.abc import (
    AbstractChannel, AbstractConnection, AbstractIncomingMessage, AbstractQueue,
)

RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USERNAME", "user")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "password")

futures = {}
async def server():
    connection = await connect(
        host='localhost',
        port=30690,
        virtualhost='/rpc',
        login=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        heartbeat=600
    )

    channel = await connection.channel()  # Create a channel

    await channel.declare_queue('rpc_queue', durable=False)  # Declare a queue
    print("RabbitMQ connection established and queue declared.")

    await channel.close()  # Close the channel
    await connection.close()  # Close the connection
    print("RabbitMQ connection closed.")

async def on_response(message: AbstractIncomingMessage) -> None:
    if message.correlation_id is None:
        print(f"Bad message {message!r}")
        return

    future: asyncio.Future = futures.pop(message.correlation_id)
    future.set_result(message.body)

async def client():
    connection = await connect(
        host='localhost',
        port=30690,
        virtualhost='/rpc',
        login=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        heartbeat=600
    )

    channel = await connection.channel()  # Create a channel
    callback_queue = await channel.declare_queue(exclusive=True)
    
    await callback_queue.consume(on_response, no_ack=True)

    correlation_id = str(uuid.uuid4())
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    futures[correlation_id] = future
    
    msg = {
        "method" : "write",
        "args": ["Objects/ConveyorHMI/ConveyorObjects/Pallets/Pallet1/destination", 3],
        "kwargs": {},
        "key": "msg_id",
    }


    await channel.default_exchange.publish(
            Message(
                json.dumps(msg).encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key="conveyor_rpc_queue",
    )
    print(f"Sent message with correlation ID: {correlation_id}")

    print("Waiting for response...")
    response = await future  # Wait for the response
    print(f"Received response: {response}")

    await channel.close()  # Close the channel
    await connection.close()  # Close the connection

if __name__ == "__main__":
    asyncio.run(client())