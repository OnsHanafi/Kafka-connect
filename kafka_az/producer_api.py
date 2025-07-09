import requests
from confluent_kafka import Producer
import json
import time

# Kafka configuration

# 1- Replace your Kafka broker(s) address here
kafka_bootstrap_servers = 'IP:9092'  # Replace your Kafka broker(s) (DEV-Kafka-server) address here 

# 2-Kafka producer configuration
producer_config = {
    'bootstrap.servers': kafka_bootstrap_servers,
    'client.id': 'kafka_producer',
}

# 3-This is the topic to which we produce our messages
# Replace with your Kafka topic name
kafka_topic = 'Dev-topic-test'   ## replaceit with your created topic , or create this one in Kafka 


# delivery_report handle delivery reports/callbacks from the Apache Kafka 
# in case err, we have "Message delivery failed:" + Error message
# in case  of delivery "Message delivered to DevopsHint [0]" 
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


# fetch_data_from_api is designed to retrieve data from an API endpoint specified by the api_url parameter
# It sends an HTTP GET request to the API endpoint using the requests.get() function from the requests library.
def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

# produce_to_kafka is responsible for producing messages to a Kafka topic.
def produce_to_kafka(data):
    producer = Producer(producer_config)

    try:
        # Produce message to Kafka topic
        producer.produce(kafka_topic, value=json.dumps(data), callback=delivery_report)

        # Wait for any outstanding messages to be delivered and delivery reports to be received.
        producer.flush()

    except Exception as e:
        print(f"Error producing to Kafka: {e}")

    #finally:
        ## Close the Kafka producer
        #producer.close()



if __name__ == "__main__":
    # Example API URL
    #api_url = "http://<>:5000/api/data"  # Replace with your actual API URL > Old Server  to generate API
    api_url = "http://IP:5000/api/data"  # Replace with your actual API URL (DEV-FLASK-API)
    # Infinite loop for continuous execution
    while True:
        try:
            # Fetch data from the API
            data = fetch_data_from_api(api_url)

            if data:
                # Produce the fetched data to the Kafka topic
                produce_to_kafka(data)
            else:
                print("Failed to fetch data from the API.")
            # Sleep 1 second for a specified interval (adjust as needed)
            time.sleep(1) 
        except KeyboardInterrupt:
            break
# flush() method ensures that all outstanding messages queued for delivery are actually transmitted to the Kafka brokers before the producer exits
producer.flush()
#close() method releases all resources used by the producer, including network connections, background threads, and internal buffers.
producer.close()

