#!/bin/bash

# Production build and run script
echo "Building production Docker image..."
docker build --target production -t ai-agents-api:prod .

echo "Starting production container..."
docker run -d \
  -p 8000:8000 \
  --name ai-agents-prod \
  --restart unless-stopped \
  ai-agents-api:prod

echo ""
echo "Production server started!"
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo ""
echo "View logs: docker logs -f ai-agents-prod"
echo "Stop: docker stop ai-agents-prod && docker rm ai-agents-prod"
