#!/bin/bash

# Development build and run script
echo "Building development Docker image..."
docker build --target development -t ai-agents-api:dev .

echo "Starting development container with hot reload..."
docker run -d \
  -p 8000:8000 \
  -v $(pwd):/app \
  -v /app/__pycache__ \
  --name ai-agents-dev \
  ai-agents-api:dev

echo ""
echo "Development server started!"
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo ""
echo "View logs: docker logs -f ai-agents-dev"
echo "Stop: docker stop ai-agents-dev && docker rm ai-agents-dev"
