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

2. Create a `.env` file with required environment variables:
   ```bash
   # Database configuration
   POSTGRES_USER=ai_agents_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=ai_agents
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432

   # OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here

   # Optional: environment and debug settings
   ENVIRONMENT=development
   DEBUG=true
   ```

3. Start with the provided scripts:
   ```bash
   # Development
   ./docker-up.sh dev

   # Production
   ./docker-up.sh prod

   # Detached mode
   ./docker-up.sh dev --detach
   ```

4. Endpoints:
   - API root: http://localhost:8000
   - OpenAPI docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Manual installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # optional: development deps
   ```

2. Set up environment variables (create `.env` file as shown above)

3. Run the server:
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

## Contributing & development

- This codebase is intended for learning and experimentation. Contributions are welcome.
- Run tests and linters if available before submitting PRs.
- See repository issues for current tasks and roadmap.

## Contact

[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-Profile-informational?style=flat&logo=linkedin&logoColor=white&color=0D76A8)](https://www.linkedin.com/in/hohuihsieh)
