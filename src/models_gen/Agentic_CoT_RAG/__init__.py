"""My Agentic CoT RAG model generator."""

from typing import Generator, List
from ..base import BaseModelGenerator
from ...models import Message
from .graph import graph


class AgenticCoTRAGModelGenerator(BaseModelGenerator):
    """Generator for My Agentic CoT RAG model."""
    
    def get_model_name(self) -> str:
        """Return the model name."""
        return "agentic-cot-rag"
    
    def generate(self, messages: List[Message]) -> Generator[str, None, None]:
        """
        Generate response tokens for My Agentic CoT RAG model.
        
        This is a placeholder implementation. Replace with actual OpenAI API call.
        
        Args:
            messages: List of conversation messages
            
        Yields:
            Generated tokens/chunks
        """
        # Initialize state
        initial_state = {
            "messages": [message.dict() for message in messages],
        }

        # Stream response generation
        for chunk in graph.stream(initial_state, stream_mode="updates", subgraphs=True):
            # Skip empty chunks or pre-model hooks
            if not chunk[0]:
                continue
            if "pre_model_hook" in chunk[1]:
                continue

            # Extract and yield the generated content
            for update in chunk[1].values():
                if "messages" in update:
                    msg = update["messages"][-1]
                    if "content" in msg:
                        yield msg["content"]