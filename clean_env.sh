#!/bin/bash

docker compose -f docker-compose.yml down
# remove all the docker containers starting with "virtualice"
echo "Removing all docker containers starting with 'virtualice'..."
docker ps -a | grep virtualice | awk '{print $1}' | xargs -I {} docker rm -f {}

# remove all the docker images starting with "virtualice"
echo "Removing all docker images starting with 'virtualice'..."
docker images | grep virtualice | awk '{print $3}' | xargs -I {} docker rmi -f {}

# # remove all the docker volumes starting with "virtualice"
echo "Removing all docker volumes starting with 'virtualice'..."
docker volume ls | grep virtualice | awk '{print $2}' | xargs -I {} docker volume rm {}

# remove the volume directories if they exist
echo "Removing volume directories from the current directory..."
if [ -d "kafka_0" ]; then
    sudo rm -r kafka_0
fi
if [ -d "kafka_1" ]; then                   
    sudo rm -r kafka_1
fi
if [ -d "kafka_2" ]; then
    sudo rm -r kafka_2
fi