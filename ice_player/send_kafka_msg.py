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

async def send_kafka_msg(bootstrap_servers: str, topic: str, msgs: list[str]):
    username = os.getenv("KAFKA_CLIENT_USER", "user")
    password = os.getenv("KAFKA_CLIENT_PASSWORD", "password")

    producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers,     
        security_protocol="SASL_PLAINTEXT", 
        sasl_mechanism="SCRAM-SHA-512", 
        sasl_plain_username=username, 
        sasl_plain_password=password,
        metadata_max_age_ms=30000,  # 30 seconds
    )

    
    try:
        await producer.start()
        for msg in msgs:
            result = await producer.send_and_wait(topic, value=msg.encode('utf-8'))
            logger.info(f"Message \"{msg}\" sent to topic \"{result.topic}\" partition {result.partition} offset {result.offset}")
    except Exception as e:
        logger.error(f"Failed to send messages: {e}")
    finally:
        await producer.stop()


def main():
    parser = argparse.ArgumentParser(description="ICE Player")
    parser.add_argument("--bootstrap-servers", type=str, default="localhost:9093", help="Kafka broker address")
    parser.add_argument("--topic", type=str, required=True, help="Topic to produce messages to")
    parser.add_argument("--msgs", type=str, nargs='+', required=True, help="Messages to send to Kafka")
    args = parser.parse_args()

    asyncio.run(send_kafka_msg(args.bootstrap_servers, args.topic, args.msgs))

if __name__ == "__main__":
    main()