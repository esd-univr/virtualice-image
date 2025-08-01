# VirtualICE Configuration

This repository contains a portable and containerized version of the data collection architecture of the ICE Laboratory.
It is designed to be used with Docker and Docker Compose, allowing for easy setup and deployment of the VirtualICE system.

## Prerequisites
- Docker: Ensure you have Docker installed on your machine. You can download it from [Docker
Install](https://docs.docker.com/get-docker/).
- Docker Compose: This is typically included with Docker Desktop, but you can also install it separately if needed. Check the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

## Getting Started
1. **Clone the Repository**:
   Open your terminal and run the following command to clone the repository:
   ```bash
   git clone https://github.com/esd-univr/virtualice-image.git
   ```
2. **Add the .envrc File**:
   Create a `.envrc` file in the root directory of the cloned repository. 
   This file is used to set environment variables for the Docker containers. 
   You can use the provided example as a template:
   
   ```bash
   touch .envrc
   echo "export KAFKA_CLIENT_USER=your_username" >> .envrc
   echo "export KAFKA_CLIENT_PASSWORD=your_password" >> .envrc
   echo "export RABBITMQ_USERNAME=your_username" >> .envrc
   echo "export RABBITMQ_PASSWORD=your_password" >> .envrc
   ```

   Once you have created the `.envrc` file, you can use `direnv` to load the environment variables automatically. 
   If you don't have `direnv` installed, you can install it from [direnv.net](https://direnv.net/).

    After installing `direnv`, run the following command to allow the environment variables:
    
    ```bash
    direnv allow
    ```
    
    Alternatively, you can manually export the variables in your terminal session:
    
    ```bash
    source .envrc
    ```

3. **Start the Docker Containers**:
   Before starting the containers, generate the configuration files by running:
   ```bash
   chmod +x generate_client_config.sh
    ./generate_client_config.sh
    ```
    
    Then, start the Docker containers using Docker Compose:
    ```bash
    docker-compose up -d
    ```

4. **Access the Services**:
    - **Kafka**: Access the Kafka service at `localhost:9093` from your local machine. Inside the Docker network, you can use the service name `kafka-0:9092`, `kafka-1:9092`, or `kafka-2:9092` to connect to the Kafka brokers.
    - **RabbitMQ**: Access the RabbitMQ management interface at `http://localhost:30690` using the credentials specified in your `.envrc` file.


5. **Send Messages to Kafka**:
   You can send spot messages to Kafka using the provided `ice_player/send_kafka_msg.py` script.

   ```bash
   python ice_player/send_kafka_msg.py --bootstrap-servers localhost:9093 --topic your_topic_name --msgs "message1" "message2"
   ```

   Alternatively, you can use the `ice_player/player.py` script to replay messages from a recording file:

   ```bash
   python ice_player/player.py --path your_recording.pkl --simulate-delays --bootstrap-servers localhost:9093 --topics list_of_topics_to_republish
   ```

   For more details on how to use these scripts use the `--help` option:

   ```bash
   python ice_player/send_kafka_msg.py --help
   python ice_player/player.py --help
   ```

**Note**: If you encounter any issues with the services not starting correctly, or if you change the docker-compose configuration, you may need to clean the local directory by running:

```bash
# stop and remove all containers if they are running
docker-compose down 

# remove all containers, networks, and volumes
chmod +x clean_env.sh
./clean_env.sh

# and then start again
docker-compose up -d
```