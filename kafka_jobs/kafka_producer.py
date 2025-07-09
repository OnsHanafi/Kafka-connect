import requests
from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = ['wn0-kafka.uvkqz5ujam0e3o0kvrniletgqb.parx.internal.cloudapp.net:9092','wn1-kafka.uvkqz5ujam0e3o0kvrniletgqb.parx.internal.cloudapp.net:9092'] 
KAFKA_TOPIC = 'yalen-topic' 
API_URL = 'http://172.18.10.2:5000/api/data' 
# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

# Fetch data from API
def fetch_data():
    try:
        # logging
        print(f"Fetching data from API")
        response = requests.get(API_URL)
        # Raise an error for bad responses
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


while True:
    # produce data to Kafka
    print("Starting data fetch and produce loop...")
    data = fetch_data()

    if data:
        for record in data:
            try:
                # Convert record to JSON string
                message = json.dumps(record).encode('utf-8')
                # Send message to Kafka topic
                producer.send(KAFKA_TOPIC, message)
                print(f"Produced message: {message}")
            except Exception as e:
                print(f"Error producing message: {e}") 
    # Make sure all data is sent
    producer.flush()

        


