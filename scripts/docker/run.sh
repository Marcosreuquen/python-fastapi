#!/bin/bash
echo "Running docker image..."
docker-compose up --build -d
echo "Docker image running."
echo "Opening logs..."
docker-compose logs -f api