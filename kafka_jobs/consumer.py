from confluent_kafka import Consumer, KafkaError
import json
import csv

# Kafka config
config = {
        # User-specific properties that you must set
        'bootstrap.servers': '40.66.41.107:9092',
        'sasl.username':     '<CLUSTER API KEY>',
        'sasl.password':     '<CLUSTER API SECRET>',

        # Fixed properties
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms':   'PLAIN',
        'group.id':          'kafka-python-getting-started',
        'auto.offset.reset': 'earliest'
    }