#!/bin/bash


# Change  to the Kafka directory 
cd /opt/kafka

# Start Zookeeper
sudo systemctl start zookeeper

# Slpeep n Seconds
sleep  7
#Start Kafka
sudo systemctl start kafka


# Save the file and make this file executable by  executing this command chmod +x start_services.sh
# important note about /etc/systemd/system/kafka.service file is executed whenever you specifically interact with the Kafka service using systemd commands, such as
# sudo systemctl start kafka: Starts the Kafka service.
# sudo systemctl stop kafka: Stops the Kafka service.
# sudo systemctl restart kafka: Restarts the Kafka service.
# sudo systemctl status kafka: Checks the status of the Kafka service.
# sudo systemctl enable kafka: Enables the Kafka service to start automatically at boot.
# sudo systemctl disable kafka: Disables the Kafka service from starting automatically at boot
# to run the command ./start_services.sh
