# Serve My Agents

*Notes: Code under construction. This repository is for learning and experimentation.*

A lightweight, OpenAI-compatible API server for running AI agents, built with FastAPI. The project aims to be a drop-in replacement for the OpenAI chat completions endpoint and supports multiple models, streaming responses, and easy deployment.

## Key features

- OpenAI-compatible chat completion API
- Support for multiple AI models (managed via LangGraph)
- Real-time streaming responses for interactive experiences
- FastAPI-based asynchronous server for performance
- Docker-friendly with compose scripts for development and production

## Quick start (recommended: Docker)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd serve-my-agents
   ```

2. Start with the provided scripts:
   ```bash
   # Development
   ./docker-dev.sh

   # Production
   ./docker-prod.sh
   ```

3. Endpoints:
   - API root: http://localhost:8000
   - OpenAPI docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Manual installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # optional: development deps
   ```

2. Run the server:
   ```bash
   python main.py
   ```

## Example request

Send a chat completion request similar to OpenAI's API:
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agentic-cot-rag",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Contact

[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-Profile-informational?style=flat&logo=linkedin&logoColor=white&color=0D76A8)](https://www.linkedin.com/in/hohuihsieh)
