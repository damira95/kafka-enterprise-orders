FROM confluentinc/cp-kafka-connect:7.6.1

# Install JDBC connector
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:latest

# Install Couchbase Kafka connector
RUN confluent-hub install --no-prompt couchbase/kafka-connect-couchbase:latest

# Default command
CMD ["bash", "-c", "connect-distributed /etc/kafka/connect-distributed.properties"]
