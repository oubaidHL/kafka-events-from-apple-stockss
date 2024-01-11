from confluent_kafka import Consumer, KafkaError
import json
from datetime import datetime

def process_message(msg):
    try:
        # Decode the message value (assuming it's a JSON string)
        message_data = json.loads(msg.value().decode('utf-8'))

        # Extract datetime from the JSON data
        yfinance_datetime = datetime.strptime(message_data['datetime'], '%Y-%m-%d %H:%M:%S')

        # Get the current time
        reception_time = datetime.now()

        # Calculate latency
        latency = reception_time - yfinance_datetime

        # Print latency
        print(f"Latency: {latency.total_seconds()} seconds")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': '192.168.0.2:9092',  # Replace with your Kafka broker address
    'group.id': 'my_consumer_group',     # Specify a consumer group ID
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False          # Disable auto-commit offsets
}

# Create a Kafka consumer instance
consumer = Consumer(consumer_conf)

# Subscribe to the pre-setup topic
consumer.subscribe(['tech'])  # Replace with your Kafka topic name

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages, timeout of 1.0 second

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Process the received message
        process_message(msg)

        # Manually commit the offset to control when to mark a message as processed
        consumer.commit(msg)

except KeyboardInterrupt:
    pass

finally:
    # Close down consumer
    consumer.close()
