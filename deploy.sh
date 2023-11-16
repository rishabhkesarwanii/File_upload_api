#!/bin/bash

# Define variables
IMAGE_NAME="my-flask-app"
CONTAINER_NAME="my-flask-container"
PORT=5000
APP_DIR="/home/rishabh/Desktop/File_upload"  # Replace this with your app's directory path
INSTANCE_DIR="$APP_DIR/instance"
UPLOADS_DIR="$APP_DIR/uploads"

# Build the Docker image
docker build -t $IMAGE_NAME .

# Stop and remove any existing container with the same name
docker stop $CONTAINER_NAME &> /dev/null
docker rm $CONTAINER_NAME &> /dev/null

# Run the Docker container with volume mounts
docker run -d -p $PORT:80 \
  -v $INSTANCE_DIR:/app/instance:rw \
  -v $UPLOADS_DIR:/app/uploads:rw \
  --name $CONTAINER_NAME $IMAGE_NAME

# Check if the container is running
if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME 2>/dev/null)" == "true" ]; then
  echo "Container $CONTAINER_NAME is running."
else
  echo "Failed to start $CONTAINER_NAME container."
  exit 1
fi
