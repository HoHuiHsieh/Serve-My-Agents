"""Streaming response utilities."""

from typing import AsyncGenerator
import time
import uuid

from ..models import (
    ChatCompletionRequest,
    ChatCompletionStreamResponse,
    StreamChoice,
    DeltaMessage
)
from .generator import generate_response


async def stream_response(request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
    """
    Generate streaming response chunks.
    
    Args:
        request: Chat completion request
        
    Yields:
        Server-Sent Event formatted response chunks
    """
    response_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())
    
    # Send initial chunk with role
    initial_chunk = ChatCompletionStreamResponse(
        id=response_id,
        created=created,
        model=request.model,
        choices=[StreamChoice(
            index=0,
            delta=DeltaMessage(role="assistant", content=""),
            finish_reason=None
        )]
    )
    yield f"data: {initial_chunk.model_dump_json()}\n\n"
    
    # Stream content token by token from generator
    for token in generate_response(request.messages, request.model):
        chunk = ChatCompletionStreamResponse(
            id=response_id,
            created=created,
            model=request.model,
            choices=[StreamChoice(
                index=0,
                delta=DeltaMessage(content=token),
                finish_reason=None
            )]
        )
        yield f"data: {chunk.model_dump_json()}\n\n"
    
    # Send final chunk
    final_chunk = ChatCompletionStreamResponse(
        id=response_id,
        created=created,
        model=request.model,
        choices=[StreamChoice(
            index=0,
            delta=DeltaMessage(),
            finish_reason="stop"
        )]
    )
    yield f"data: {final_chunk.model_dump_json()}\n\n"
    yield "data: [DONE]\n\n"
