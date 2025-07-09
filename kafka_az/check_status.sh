#!/bin/bash

# Check the status of Zookeeper
echo "Checking the status of Zookeeper..."
sudo systemctl status zookeeper --no-pager

sleep 2
# Check the status of Kafka
echo "Checking the status of Kafka..."
sudo systemctl status kafka  --no-pager

#The --no-pager option in the systemctl command is used to display the output directly to the terminal without invoking a pager such as less or more. This can be particularly 
#useful when you want to see the entire output immediately without needing to scroll through it interactively.
