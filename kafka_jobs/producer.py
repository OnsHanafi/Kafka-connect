import os
import json
from confluent_kafka import Producer
# from kafka import KafkaProducer
import socket
import time

import logging
logging.basicConfig(level=logging.DEBUG)

# Working directory 
current_dir = '../output_test'
# Kafka configuration
KAFKA_BROKER = ['wn0-kafka.uvkqz5ujam0e3o0kvrniletgqb.parx.internal.cloudapp.net:9092','wn1-kafka.uvkqz5ujam0e3o0kvrniletgqb.parx.internal.cloudapp.net:9092']  # Replace with your Kafka broker address
                
conf = {
    'bootstrap.servers': KAFKA_BROKER, 
    # 'security.protocol': 'SASL_SSL',
    # 'sasl.mechanisms': 'PLAIN',
    # 'sasl.username': 'admin',  # or your Kafka username
    # 'sasl.password': 'Kafka@1234',  # or your actual password
    'client.id': socket.gethostname(),
    # 'socket.connect.timeout.ms': 5000,
    # 'socket.timeout.ms': 10000,
    # 'metadata.request.timeout.ms': 3000,
    # 'message.timeout.ms': 10000,
    'debug': 'generic,broker,security,protocol,topic,metadata',
}

producer = Producer(conf)
producer.produce('yalen-test', value='test message')
producer.flush()

# # test
    # producer = KafkaProducer(
    #     bootstrap_servers='10.0.0.8:9092',
    #     security_protocol='PLAINTEXT'

    #     )
    # # Send test messages to Kafka
    # for _ in range(5):
    #     producer.send('test', b'test message')
    #     print("Message sent")
    # producer.flush()

# Create Producer instance
# producer = Producer(conf)

# Function to send data to Kafka
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition}] at offset {msg.offset()}")
### ___Checkpoint___ ### 
def save_checkpoint(checkpoint):
    try:
        with open("checkpoint.txt", 'w') as f:
            f.write('\n'.join(checkpoint))
    except FileNotFoundError:
        return None
def read_checkpoint():
    try:
        with open("checkpoint.txt","r") as f:
           return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set() 

# Keep monitoring files, program only exited manually
# while True:    
    # processed_files = read_checkpoint()
    # Iterate through all the files in the current_dir
# for filename in os.listdir(current_dir):
#     if filename.endswith('.json'): 
#     # and filename not in processed_files:
#         file_path = os.path.join(current_dir, filename)
#         with open(file_path, 'r') as json_file:
#             try:
#                 data = json.load(json_file)  # Load JSON data
#                 # Produce JSON content to Kafka
#                 save_checkpoint(filename) #Save file to ckeckpoint
#                 producer.produce('test', value=json.dumps(data), callback=delivery_report)
#             except json.JSONDecodeError as e:
#                 print(f"Error decoding JSON from {filename}: {e}")  
#     else:
#         print("No Files To Send.......")  
# # Deliver all messages
# producer.flush()
#     # time.sleep(5)                

