"""Connection setup for Agentic CoT RAG model components."""
from langchain_postgres import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings, ChatOpenAI
from database import db_manager
from .config import vectorstore_config, chatmodel_config, embedding_model_config


# Initialize the chat completion connection
chat_model = ChatOpenAI(**chatmodel_config)

# Initialize the embedding model connection
embeddings = OpenAIEmbeddings(**embedding_model_config)

# Initialize the vector store connection
vectorstore = PGVector(
    **vectorstore_config,
    connection=db_manager._engine,
)
