"""Model generators package."""

from .base import BaseModelGenerator
from .Agentic_CoT_RAG import AgenticCoTRAGModelGenerator


# Model registry
MODEL_REGISTRY = {
    "agentic-cot-rag": AgenticCoTRAGModelGenerator,
}


__all__ = [
    "BaseModelGenerator",
    "MODEL_REGISTRY",
]
