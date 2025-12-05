"""Main entry point for the AI Agents application."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from src.models import (
    ChatCompletionRequest,
)
from src.core.completion import create_chat_completion
from src.core.streaming import stream_response

app = FastAPI(
    title="AI Agents API",
    description="OpenAI-compatible API for AI Agents",
    version="0.1.0"
)


# ====================
# API Endpoints
# ====================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Agents API - OpenAI Compatible",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "models": "/v1/models",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "AI Agents API"}
    )


@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI compatible)."""
    return {
        "object": "list",
        "data": [
            {
                "id": "gpt-3.5-turbo",
                "object": "model",
                "created": 1677610602,
                "owned_by": "ai-agents"
            },
            {
                "id": "gpt-4",
                "object": "model",
                "created": 1687882411,
                "owned_by": "ai-agents"
            }
        ]
    }


@app.post("/v1/chat/completions", response_model=None)
async def chat_completions(request: ChatCompletionRequest):
    """
    Create a chat completion (OpenAI compatible).
    Supports both streaming and non-streaming responses.
    """
    try:
        # Streaming response
        if request.stream:
            return StreamingResponse(
                stream_response(request),
                media_type="text/event-stream"
            )
        
        # Non-streaming response
        response = create_chat_completion(
            messages=request.messages,
            model=request.model
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # For development with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
