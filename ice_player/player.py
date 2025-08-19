import os 
import asyncio
from aiokafka import AIOKafkaProducer, ConsumerRecord
import argparse
import pickle
from datetime import datetime
import time
from typing import AsyncGenerator, Generator
import logging

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)

class ICEPlayer():

    def __init__(self, path: str, topics: list[str]):
        with open(path,'rb') as f:
            msgs_list: list[ConsumerRecord] = pickle.load(f)

        self._topics = topics
        self._msgs_list = [msg for msg in msgs_list if msg.topic in topics]

    def get_messages(self, simulate_delays: bool=True) -> Generator[ConsumerRecord, None, None]:
        msgs_list = self._msgs_list
        delay = 0

        yield msgs_list[0]

        for i in range(1,len(msgs_list)):
            if simulate_delays:
                delay = datetime.fromtimestamp(msgs_list[i].timestamp/1000)-datetime.fromtimestamp(msgs_list[i-1].timestamp/1000)
                delay = delay.total_seconds()
                if delay > 0:
                    time.sleep(delay)
            
            yield msgs_list[i]


    async def get_messages_async(self, simulate_delays: bool=True) -> AsyncGenerator[ConsumerRecord, None]:
        msgs_list = self._msgs_list
        delay = 0

        yield msgs_list[0]

        for i in range(1,len(msgs_list)):
            if simulate_delays:
                delay = datetime.fromtimestamp(msgs_list[i].timestamp/1000)-datetime.fromtimestamp(msgs_list[i-1].timestamp/1000)
                delay = delay.total_seconds()
                if delay > 0:
                    await asyncio.sleep(delay)

            yield msgs_list[i]

    async def produce_messages(self, producer: AIOKafkaProducer, simulate_delays: bool=True):
        async for msg in self.get_messages_async(simulate_delays):
            result = await producer.send(
                topic=msg.topic,
                value=msg.value,
                key=msg.key
            )
            result = await result

            logger.info(f"Produced message to {msg.topic} with value {msg.value} at offset {result.offset}")


async def start_producer(path: str, topics: list[str], simulate_delays: bool, bootstrap_servers: str, infinite: bool):
    username = os.getenv("KAFKA_CLIENT_USER", "user")
    password = os.getenv("KAFKA_CLIENT_PASSWORD", "password")
    logger.info(f"Using Kafka broker: {bootstrap_servers}")
    logger.info(f"Using Kafka username: {username}")
    logger.info(f"Using Kafka password: {password}")
    logger.info(f"Selected topics: {topics}")
    if infinite:
        logger.warning("Infinite mode is enabled. Messages will be produced indefinitely.")

    producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers,     
        security_protocol="SASL_PLAINTEXT", 
        sasl_mechanism="SCRAM-SHA-512", 
        sasl_plain_username=username, 
        sasl_plain_password=password,
        metadata_max_age_ms=30000,  # 30 seconds
    )
    try:
        await producer.start()
        ice_player = ICEPlayer(path, topics)
        
        while True:
            await ice_player.produce_messages(producer, simulate_delays)
            if not infinite:
                break
            # Sleep for a while before producing the next batch of messages
            await asyncio.sleep(1)
    
    finally:
        await producer.stop()


def main():
    parser = argparse.ArgumentParser(description="ICE Player")
    parser.add_argument("--path", type=str, required=True, help="Path to the pickle file containing messages")
    parser.add_argument("--topics", type=str, nargs='+', required=True, help="List of topics to filter messages")
    parser.add_argument("--simulate-delays", action='store_true', help="Simulate delays between messages")
    parser.add_argument("--bootstrap-servers", type=str, default="localhost:9093", help="Kafka broker address")
    parser.add_argument("--infinite", action='store_true', help="Run the producer in infinite mode")
    args = parser.parse_args()

    asyncio.run(start_producer(args.path, args.topics, args.simulate_delays, args.bootstrap_servers, args.infinite))

if __name__ == "__main__":
    main()