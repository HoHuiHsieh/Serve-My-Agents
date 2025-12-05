"""Pydantic models for OpenAI-compatible API."""

from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message model."""
    role: Literal["system", "user", "assistant", "function"]
    content: str
    name: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    """Chat completion request model (OpenAI compatible)."""
    model: str = Field(default="gpt-3.5-turbo", description="Model to use")
    messages: List[Message] = Field(..., description="List of messages")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1)
    n: Optional[int] = Field(default=1, ge=1, le=10)
    stream: Optional[bool] = Field(default=False)
    stop: Optional[List[str]] = None
    max_tokens: Optional[int] = Field(default=None, ge=1)
    presence_penalty: Optional[float] = Field(default=0, ge=-2, le=2)
    frequency_penalty: Optional[float] = Field(default=0, ge=-2, le=2)
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None


class Usage(BaseModel):
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Choice(BaseModel):
    """Response choice model."""
    index: int
    message: Message
    finish_reason: Literal["stop", "length", "content_filter", "null"]


class ChatCompletionResponse(BaseModel):
    """Chat completion response model (OpenAI compatible)."""
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class DeltaMessage(BaseModel):
    """Streaming delta message."""
    role: Optional[str] = None
    content: Optional[str] = None


class StreamChoice(BaseModel):
    """Streaming response choice."""
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length", "content_filter", "null"]] = None


class ChatCompletionStreamResponse(BaseModel):
    """Streaming chat completion response (OpenAI compatible)."""
    id: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int
    model: str
    choices: List[StreamChoice]
