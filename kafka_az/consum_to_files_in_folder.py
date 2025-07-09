from confluent_kafka import Consumer, KafkaError
import json
import csv

# Kafka configuration
kafka_config = {
    'bootstrap.servers': '<IP>:9092',  # Replace it with Kafka Server Dev-Kafka-server
    'group.id': 'console-consumer-15633', # Reuse the same group ID or choose a new one
    'auto.offset.reset': 'earliest'
}

# Kafka consumer
consumer = Consumer(kafka_config)
topics = ['Dev-topic-test']
consumer.subscribe(topics)

# Initialize variables for CSV file handling
record_count = 0
file_count = 1
max_records_per_file = 10   # How many records per file 

# Read and process Kafka messages
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    # Decode and process JSON message
    try:
        data = json.loads(msg.value().decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        continue

    # Prepare CSV data
    csv_data = ",".join(str(value) for value in data.values())

    # Write to CSV file
    filename = f'/opt/projects/python_pro/outputfiles/file{file_count}.csv'
    with open(filename, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header for the first record in the file
        if record_count == 0:
            csv_writer.writerow(data.keys())

        # Write data
        csv_writer.writerow(data.values())

    # Update counters
    record_count += 1

    # Check if it's time to start a new file
    if record_count >= max_records_per_file:
        record_count = 0
        file_count += 1
        print(filename)

# Close Kafka consumer
consumer.close()
