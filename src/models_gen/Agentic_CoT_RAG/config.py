"""Default configurations for Agentic CoT RAG model generator."""

# Embedding model configuration
embedding_model_config = {
    "model": "text-embedding-3-small",
}

# Vector store configuration
vectorstore_config = {
    "collection_name": "my_docs",
    "use_jsonb": True,
    "pre_delete_collection": False,
}

# Chat model configuration
chatmodel_config = {
    "model": "gpt-5-nano",
    "max_completion_tokens": 4096,
}
