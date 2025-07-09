from kafka import KafkaConsumer
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import json


# Kafka configuration
KAFKA_BROKER = ['wn0-kafka.uvkqz5ujam0e3o0kvrniletgqb.parx.internal.cloudapp.net:9092','wn1-kafka.uvkqz5ujam0e3o0kvrniletgqb.parx.internal.cloudapp.net:9092'] 
KAFKA_TOPIC = 'yalen-topic' 
GROUP_ID = 'yalen-consumer-group'
# Azure configuration
AZURE_STORAGE_ACCOUNT_NAME = 'kafkaclusterstorage'
AZURE_STORAGE_CONTAINER_NAME = 'data-output'
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=kafkaclusterstorage;AccountKey=sUtpjlAj3g6I3YkSqG5PXnDviYiA6MiFgPxNIGUz90GIl2rbcrIPuFq6kn3n6s6dCKzbBrEuFkZa+ASt9q56HQ==;EndpointSuffix=core.windows.net"

# Consumer configuration
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=GROUP_ID,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
    
# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
print("Connected to Azure Blob Storage")
container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
print(f'Using container: {AZURE_STORAGE_CONTAINER_NAME}')

# Create the container if it does not exist
try:
    container_client.create_container()
except Exception:
    pass  # Already exists

print("##########################################################")
print(f"Listening for messages...................")

# Function to append data to blob by scan_id
def append_to_blob(scan_id, new_entry):
    blob_name = f"scan_report_{scan_id}.json"
    blob_client = container_client.get_blob_client(blob_name)

    existing_data = []

    if blob_client.exists():
        download_stream = blob_client.download_blob()
        existing_data = json.loads(download_stream.readall())
        if not isinstance(existing_data, list):
            existing_data = [existing_data]

    existing_data.append(new_entry)

    # Convert updated list back to JSON
    updated_data_bytes = json.dumps(existing_data, indent=2).encode('utf-8')
    blob_client.upload_blob(updated_data_bytes, overwrite=True)
    print(f"Appended to blob: {blob_name}")


# Consume data
# Start consuming
for message in consumer:
    data_batch = message.value  

    if isinstance(data_batch, list):
        for data in data_batch:
            scan_id = data.get("scan_id")
            if scan_id:
                append_to_blob(scan_id, data)
    else:
        print("Message format is invalid expected a list")