#!/usr/bin/env python3
"""
Kafka producer for streaming transaction data.
"""

import json
import logging
import random
from datetime import datetime
from time import sleep

try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None


def generate_transaction():
    return {
        "transaction_id": f"TX{random.randint(100000, 999999)}",
        "customer_id": f"C{random.randint(100, 999)}",
        "agent_id": f"A{random.randint(10, 99)}",
        "transaction_date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(random.uniform(10, 5000), 2),
        "status": random.choice(["success", "pending", "failed"]),
    }


def produce_streaming_data(bootstrap_servers="localhost:9092", topic="transactions", interval=5):
    if KafkaProducer is None:
        logging.error("kafka-python is not installed")
        return

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    logging.info(f"Starting to produce to {topic} on {bootstrap_servers}")

    try:
        while True:
            tx = generate_transaction()
            producer.send(topic, tx)
            producer.flush()
            logging.info(f"Produced: {tx['transaction_id']}")
            sleep(interval)
    except KeyboardInterrupt:
        logging.info("Stopping producer")
    finally:
        producer.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    produce_streaming_data()
