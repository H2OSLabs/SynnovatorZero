#!/bin/bash

# Deploy script for SynnovatorZero

# Check if .env file exists
if [ ! -f ../.env ]; then
    echo "Creating .env file from example..."
    if [ -f ../.env.example ]; then
        cp ../.env.example ../.env
    else
        echo "Error: .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Build and start services
echo "Starting services..."
docker compose up -d --build

echo "Deployment complete."
