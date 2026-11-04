#!/usr/bin/env python3
"""
Kafka producer for streaming transaction data to the raw transactions topic.
"""

import json
import logging
import random
from datetime import datetime

try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None


RAW_TOPIC = "transactions.raw"


def generate_transaction():
    return {
        "transaction_id": f"TX{random.randint(100000, 999999)}",
        "customer_id": f"C{random.randint(100, 999)}",
        "agent_id": f"A{random.randint(10, 99)}",
        "region": random.choice(["Nairobi", "Mombasa", "Kisumu", "Nakuru"]),
        "transaction_date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(random.uniform(10, 5000), 2),
        "currency": "KES",
        "status": random.choice(["success", "pending", "failed"]),
        "payment_method": random.choice(["Mpesa", "mobile_money", "card"]),
        "event_time": datetime.utcnow().isoformat() + "Z",
    }


def produce(bootstrap_servers="localhost:9092", topic=RAW_TOPIC, count=10, interval=1):
    if KafkaProducer is None:
        logging.error("kafka-python is not installed")
        return []

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda v: v.encode("utf-8") if v else None,
    )

    messages = []
    for _ in range(count):
        tx = generate_transaction()
        producer.send(topic, key=tx["transaction_id"], value=tx)
        producer.flush()
        messages.append(tx)
        logging.info(f"Produced to {topic}: {tx['transaction_id']}")

    producer.close()
    return messages


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    produce()
