import logging
import json
from typing import Optional

from confluent_kafka import Consumer, KafkaException


def create_consumer(
    bootstrap_servers: str,
    group_id: str,
    topic: str,
) -> Optional[Consumer]:
    try:
        import confluent_kafka
    except ImportError:
        logging.error("confluent-kafka is not installed. Install with: pip install confluent-kafka")
        return None

    conf = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(conf)
    consumer.subscribe([topic])
    logging.info(f"Subscribed to Kafka topic: {topic}")
    return consumer


def consume_transactions(
    bootstrap_servers: str,
    group_id: str,
    topic: str,
    max_messages: int = 100,
) -> list:
    consumer = create_consumer(bootstrap_servers, group_id, topic)
    if consumer is None:
        return []

    messages = []
    try:
        for i in range(max_messages):
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                break
            if msg.error():
                raise KafkaException(msg.error())

            record = json.loads(msg.value().decode("utf-8"))
            messages.append(record)
            logging.info(f"Consumed message {i + 1}: {record.get('transaction_id', 'N/A')}")

    finally:
        consumer.close()

    logging.info(f"Consumed {len(messages)} messages from {topic}")
    return messages
