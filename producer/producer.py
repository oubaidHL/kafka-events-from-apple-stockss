import yfinance as yf
from confluent_kafka import Producer, KafkaError
import json
import time
from datetime import datetime

# Configure the Kafka producer
kafka_bootstrap_servers = "192.168.0.2:9092"  # Replace with your Kafka broker address
topic_name = 'tech'
producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})

def fetch_and_send_stock_prices():
    try:
        # Read Apple stock prices
        apple_stock = yf.Ticker("AAPL")
        minute_data = apple_stock.history(period='1d', interval='1m')['Close'].tail(5)

        # Generate a JSON with the latest 5-minute prices
        data = {'symbol': 'AAPL', 'minute_prices': minute_data.tolist(), 'datetime': str(datetime.now())}
        data_json = json.dumps(data)

        # Send the JSON to the Kafka topic
        producer.produce(topic_name, key='key', value=data_json, callback=delivery_report)

    except Exception as e:
        print(f"Error fetching and sending data: {e}")

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    while True:
        fetch_and_send_stock_prices()
        producer.flush()
        time.sleep(60)  # Wait for 1 minute before fetching and sending data again
