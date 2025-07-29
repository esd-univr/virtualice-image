#!/bin/bash

# Source environment variables
source .envrc

# Generate client.properties file
cat > kafka/client.properties << EOF
bootstrap.servers=localhost:9092
security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-512

sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \\
    username="${KAFKA_CLIENT_USER}" \\
    password="${KAFKA_CLIENT_PASSWORD}";
EOF

echo "Generated kafka/client.properties with environment variables"
