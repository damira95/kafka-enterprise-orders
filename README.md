Kafka Enterprise Orders
Real-Time Event-Driven Order Processing Platform (Confluent Stack)
📌 Overview
This project implements a production-style event-driven microservices platform using Apache Kafka (Confluent ecosystem).
It demonstrates:
Decoupled microservices communication
Real-time stream processing
Data ingestion & sink pipelines via Kafka Connect
Streaming transformations using ksqlDB
Polyglot persistence (Postgres + Couchbase)
Containerized distributed system simulation
The architecture mirrors real-world systems used in fintech, e-commerce, and mobility platforms.
🏗 Architecture
Core Event Flow
order-producer → Kafka (orders topic)

payment-service   → consumes orders → emits payments
fraud-service     → consumes orders → emits fraud alerts
analytics-service → consumes orders → updates counters

Kafka → ksqlDB → order-analytics topic
Kafka → Couchbase Sink → Couchbase bucket
Postgres → JDBC Source → Kafka
🧩 Confluent Stack Components
Kafka Broker
Zookeeper
Schema Registry
Kafka Connect
ksqlDB Server
Confluent Control Center
Kafdrop (topic inspection UI)
This setup simulates a distributed streaming platform locally via Docker Compose.
📁 Repository Structure
kafka-enterprise-orders/
├── docker-compose.yml
├── .env
├── db/
│   └── init.sql
├── connect/
│   ├── Dockerfile
│   └── connectors/
│       ├── jdbc-source.json
│       └── couchbase-sink.json
├── ksql/
│   └── streams.sql
├── producer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── order_producer.py
└── consumers/
    ├── fraud-service/
    ├── payment-service/
    └── analytics-service/

