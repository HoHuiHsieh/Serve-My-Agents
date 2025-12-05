"""Response generation utilities."""

from typing import List, Generator
from ..models import Message
from ..models_gen import MODEL_REGISTRY, BaseModelGenerator


def get_model_generator(model: str) -> BaseModelGenerator:
    """
    Get the appropriate model generator based on model name.

    Args:
        model: Model name

    Returns:
        Model generator instance

    Raises:
        ValueError: If model is not supported
    """
    generator_class = MODEL_REGISTRY.get(model)
    if generator_class is None:
        raise ValueError(f"Model '{model}' is not supported.")

    return generator_class()


def generate_response(messages: List[Message], model: str) -> Generator[str, None, None]:
    """
    Generate a response based on the messages.
    Returns a generator that yields tokens/chunks.

    Args:
        messages: List of conversation messages
        model: Model name to use

    Yields:
        Generated tokens/chunks
    """
    # Get the appropriate generator for the model
    generator = get_model_generator(model)

    # Yield tokens from the generator
    yield from generator.generate(messages)
