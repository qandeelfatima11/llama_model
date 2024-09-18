#!/bin/bash

# Get the container ID of the running LLaMA training service
# container_id=$(docker-compose ps -q llama_training_container)

container_id=$(docker-compose ps -q llama_training)

# container_id="988e2a783328"
# Check if the container ID is found
if [ -z "$container_id" ]; then
    echo "Error: Container for 'llama_training_container' not found."
    exit 1
fi

# Define the prompt
prompt="scope of datascience"
no_of_cores= [0]

# Generate a unique log file name based on the prompt and timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")
log_file="docker_stats_${prompt// /_}_${timestamp}_${no_of_cores}.log"

# Create the stats directory if it does not exist
if [ ! -d "./stats" ]; then
    mkdir -p "./stats"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create directory ./stats."
        exit 1
    fi
fi

# Start logging Docker stats every minute
echo "Prompt: $prompt with number of cores: $no_of_cores " > "./stats/$log_file"  # Write prompt to file

# Write header to log file only once
docker stats "$container_id" --no-stream | head -n 1 >> "./stats/$log_file"

while true; do
    # Append Docker stats to the log file every minute
    docker stats "$container_id" --no-stream | tail -n +2 >> "./stats/$log_file"  # Log stats without header
    echo "" >> "./stats/$log_file"  # Add a new line for readability
    sleep 60
done
