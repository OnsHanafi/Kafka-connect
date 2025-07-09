#!/bin/bash


# Change  to the Kafka directory 
cd /opt/kafka

#run consumer command
sudo bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic DevopsHint --from-beginning
#Save the file and make this file executable by  executing this command chmod +x  start_consumer.sh
