import os 
import asyncio
from aiokafka import AIOKafkaConsumer

KAFKA_CLIENT_USER = os.getenv("KAFKA_CLIENT_USER", "user")
KAFKA_CLIENT_PASSWORD = os.getenv("KAFKA_CLIENT_PASSWORD", "password")

async def consume_messages():
    consumer = AIOKafkaConsumer(
        'ice_data_conveyor_state',
        bootstrap_servers='localhost:9093',
        group_id='test-consumer-group',
        security_protocol="SASL_PLAINTEXT", 
        sasl_mechanism="SCRAM-SHA-512", 
        sasl_plain_username=KAFKA_CLIENT_USER, 
        sasl_plain_password=KAFKA_CLIENT_PASSWORD,
    )
    
    await consumer.start()
    
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode('utf-8')}")
            print(f"Topic: {message.topic}, Partition: {message.partition}, Offset: {message.offset}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())