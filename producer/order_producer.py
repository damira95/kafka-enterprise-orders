import json
import os
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def get_env(name: str, default: str) -> str:
    value = os.environ.get(name)
    if not value:
        return default
    return value


KAFKA_BROKER = get_env("KAFKA_BROKER", "kafka:9092")
ORDERS_TOPIC = get_env("ORDERS_TOPIC", "orders")
INTERVAL_SECONDS = float(get_env("ORDER_PRODUCER_INTERVAL_SECONDS", "3"))


def create_producer() -> KafkaProducer:
    """
    Kafka даяр болгонго чейин retry кыла турган producer.
    """
    while True:
        try:
            print(f"[order-producer] Trying to connect to Kafka at {KAFKA_BROKER} ...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: str(k).encode("utf-8"),
            )
            # Бир жолу metadata алып көрүп, чындап туташты бекитебиз
            producer.bootstrap_connected()
            print(f"[order-producer] ✅ Connected to Kafka at {KAFKA_BROKER}, topic '{ORDERS_TOPIC}'")
            return producer
        except NoBrokersAvailable:
            print(f"[order-producer] ❌ Kafka not ready yet at {KAFKA_BROKER}, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"[order-producer] ❌ Unexpected error connecting to Kafka: {e}")
            time.sleep(5)


def random_country() -> str:
    countries = ["US", "CA", "GB", "DE", "FR", "RU", "BR", "AU", "IN"]
    return random.choice(countries)


def random_currency() -> str:
    return "USD"


def random_customer_id() -> int:
    return random.randint(1000, 9999)


def random_amount() -> float:
    return round(random.uniform(10, 600), 2)


def random_source() -> str:
    return random.choice(["web", "mobile", "api"])


def generate_order(order_id: int) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    order = {
        "order_id": order_id,
        "customer_id": random_customer_id(),
        "amount": random_amount(),
        "currency": random_currency(),
        "country": random_country(),
        "status": "NEW",
        "created_at": now,
        "source": random_source(),
    }
    return order


def main():
    print(f"[order-producer] Starting order producer, broker={KAFKA_BROKER}, topic={ORDERS_TOPIC}")
    producer = create_producer()
    order_id = 1

    while True:
        order = generate_order(order_id)
        producer.send(ORDERS_TOPIC, key=order["order_id"], value=order)
        producer.flush()
        print(f"[order-producer] Sent order: {order}")
        order_id += 1
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
