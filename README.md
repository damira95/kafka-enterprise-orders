flowchart LR
    OP[order-producer] -->|orders| K((Kafka Broker))
    PS[payment-service] -->|consume orders| K
    FS[fraud-service] -->|consume orders| K
    AS[analytics-service] -->|consume orders| K

    K -->|order-analytics| CB[(Couchbase)]

    PG[(Postgres)] -->|JDBC Source Connector| K
    K -->|Couchbase Sink Connector| CB

    subgraph Confluent Stack
        ZK[Zookeeper]
        SR[Schema Registry]
        KC[Kafka Connect]
        KSQL[ksqlDB Server]
        CC[Control Center]
    end

    ZK --> K
    KC --> K
    SR --> K
    KSQL --> K
    CC --> K
📁 2. Repository Structure
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

# Future additions
├── web/
│   ├── backend/                 # FastAPI backend API (Part 4)
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routes/
│   │   │   ├── services/
│   │   │   └── models/
│   │   └── Dockerfile
│
│   └── frontend/               # React dashboard (Part 4)
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── hooks/
│       │   └── services/
│       └── Dockerfile
│
├── infra/terraform/            # AWS VPC, ECS, RDS, WAF, AMP, etc.
├── k8s/charts/webapp/          # Helm chart for frontend/backend
├── argocd/                     # GitOps deployment config
└── .github/workflows/          # CI/CD pipeline
⚙️ 3. Running the System (Local)
3.1 Start everything
docker-compose up -d --build
3.2 Initialize Couchbase
Open http://localhost:8091
Credentials:
Username: Administrator
Password: password
Create bucket: order_analytics
3.3 Useful UIs
Service	URL
Kafdrop	http://localhost:9000
Control Center	http://localhost:9021
Schema Registry	http://localhost:8081
ksqlDB Server	http://localhost:8088/info
Couchbase	http://localhost:8091
🔌 4. Kafka Connect Pipelines
JDBC Source → Postgres → Kafka
curl -X POST -H "Content-Type: application/json" \
  --data @connect/connectors/jdbc-source.json \
  http://localhost:8083/connectors
Couchbase Sink → Kafka → Couchbase
curl -X POST -H "Content-Type: application/json" \
  --data @connect/connectors/couchbase-sink.json \
  http://localhost:8083/connectors
🧠 5. Microservices Overview
order-producer
Generates orders every N seconds
Publishes to orders topic
payment-service
Consumes orders
Simulates payment
Publishes to payments
fraud-service
Consumes orders
Flags risky orders based on rules
analytics-service
Consumes orders
Maintains counters, totals
Optionally writes to Couchbase
📊 6. ksqlDB Streaming Logic
Defined in ksql/streams.sql:
ORDERS_STREAM
Aggregations: count, sum by country
Output → order-analytics topic
🧪 7. Checking Logs
docker logs -f order-producer
docker logs -f payment-service
docker logs -f fraud-service
docker logs -f analytics-service
Expect: orders → fraud alerts → payment events → analytics updates.
☁️ 8. Future Phases (Cloud Roadmap)
Part 2 – Deploy to AWS EC2 (most affordable)
Run full stack on one EC2 instance
Docker + Docker Compose
Nginx reverse proxy
Optional domain + HTTPS
Part 3 – Full AWS (ECS + Confluent Cloud)
Microservices → ECS Fargate
Database → RDS Postgres
Kafka → Confluent Cloud
AWS Secrets Manager
Autoscaling
Terraform IaC
GitHub Actions CI/CD
Part 4 – Public Dashboard
FastAPI backend
React frontend
Deploy to EKS
Helm charts
ArgoCD GitOps
Part 5 – Observability
AWS Managed Prometheus (AMP)
AWS Managed Grafana (AMG)
AWS OTel Collector sidecar
🎙️ 9. Interview Summary (2-minute story)
*“I built a full event-driven real-time orders platform using Confluent Kafka.
The system includes multiple microservices—order-producer, payment-service, fraud-service, and analytics-service—communicating through Kafka topics.
I implemented real-time ingestion from Postgres to Kafka using a JDBC Source Connector, and real-time delivery from Kafka to Couchbase using a Couchbase Sink Connector.

Everything runs locally inside Docker Compose: Kafka Broker, Zookeeper, Schema Registry, Kafka Connect, ksqlDB Server + CLI, Confluent Control Center, Kafdrop, Postgres, Couchbase, and four Python microservices.

I also built streaming transformations and aggregations using ksqlDB to produce an order-analytics topic.

This architecture mirrors real systems used at Uber, Netflix, banking, and e-commerce companies.

The next stage moves this entire ecosystem to AWS using EC2/ECS, RDS, Terraform IaC, GitHub Actions CI/CD, and ArgoCD GitOps.”*
