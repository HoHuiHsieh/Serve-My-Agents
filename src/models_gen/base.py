"""Base model generator interface."""

from typing import Generator, List
from abc import ABC, abstractmethod
from ..models import Message


class BaseModelGenerator(ABC):
    """Base class for model generators."""
    
    @abstractmethod
    def generate(self, messages: List[Message]) -> Generator[str, None, None]:
        """
        Generate response tokens.
        
        Args:
            messages: List of conversation messages
            
        Yields:
            Generated tokens/chunks
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model name."""
        pass
