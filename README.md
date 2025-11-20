## 📂 Project Structure

```text
.
├── connect
│   ├── Dockerfile
│   └── connectors
│       ├── couchbase-sink.json
│       └── jdbc-source.json
├── consumers
│   ├── analytics-service
│   │   ├── Dockerfile
│   │   ├── analytics_consumer.py
│   │   └── requirements.txt
│   ├── fraud-service
│   │   ├── Dockerfile
│   │   ├── fraud_consumer.py
│   │   └── requirements.txt
│   └── payment-service
│       ├── Dockerfile
│       ├── payment_consumer.py
│       └── requirements.txt
├── db
│   └── init.sql
├── docker-compose.yml
├── ksql
│   └── streams.sql
└── producer
    ├── Dockerfile
    ├── order_producer.py
    └── requirements.txt
```

