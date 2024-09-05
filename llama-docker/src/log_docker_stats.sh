#!/bin/bash
echo "Monitoring Docker stats for LLaMA training..."
while true; do
    docker stats llama_training_container --no-stream >> src/stats/docker_stats.log
    sleep 60  # Log every 60 seconds
done
