# Use Confluent official Docker image for Kafka (Community Version)
FROM confluentinc/cp-kafka:latest

# Set environment variables for Kafka
ENV KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true

# Expose Kafka port
EXPOSE 9092

# Run Kafka server
CMD ["sh", "-c", "echo 'Waiting for Kafka to start...'; sleep 30; kafka-topics.sh --create --topic tech --partitions 1 --replication-factor 1 --bootstrap-server kafka:9092; echo 'Topic tech created.'; kafka-topics.sh --list --bootstrap-server kafka:9092; /etc/confluent/docker/run"]
