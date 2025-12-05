"""Non-streaming response utilities."""

import time
import uuid
from typing import List

from ..models import (
    Message,
    ChatCompletionResponse,
    Choice,
    Usage
)
from .generator import generate_response
from .tokenizer import estimate_tokens


def create_chat_completion(
    messages: List[Message],
    model: str
) -> ChatCompletionResponse:
    """
    Create a non-streaming chat completion response.
    
    Args:
        messages: List of conversation messages
        model: Model name to use
        
    Returns:
        ChatCompletionResponse with generated content and usage info
    """
    # Generate unique response ID
    response_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())
    
    # Generate response - collect all tokens from generator
    assistant_message = "".join(generate_response(messages, model))
    
    # Calculate token usage
    prompt_text = " ".join([msg.content for msg in messages])
    prompt_tokens = estimate_tokens(prompt_text)
    completion_tokens = estimate_tokens(assistant_message)
    
    # Build response
    response = ChatCompletionResponse(
        id=response_id,
        created=created,
        model=model,
        choices=[Choice(
            index=0,
            message=Message(role="assistant", content=assistant_message),
            finish_reason="stop"
        )],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens
        )
    )
    
    return response
