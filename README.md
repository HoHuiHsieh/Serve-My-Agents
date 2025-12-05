# Serve My Agents

An OpenAI-compatible API server for AI agents, built with FastAPI.

## Features

- **OpenAI-Compatible API**: Drop-in replacement for OpenAI's chat completion API
- **Multiple AI Models**: Support for various AI models managed via LangGraph
- **Streaming Support**: Real-time streaming responses for interactive experiences
- **FastAPI Framework**: High-performance async API built on FastAPI
- **Docker Ready**: Easy deployment with Docker and docker-compose

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd serve-my-agents
   ```

2. **Start with Docker Compose**
   ```bash
   # For development
   ./docker-dev.sh

   # For production
   ./docker-prod.sh
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

### Manual Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

2. **Run the server**
   ```bash
   python main.py
   ```

3. **Test the API**
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
