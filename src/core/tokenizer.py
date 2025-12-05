"""Token estimation utilities."""


def estimate_tokens(text: str) -> int:
    """
    Estimate token count (rough approximation).
    
    Args:
        text: Input text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    # Simple approximation: word count + character count / 4
    return len(text.split()) + len(text) // 4
