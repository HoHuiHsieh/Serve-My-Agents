"""Define tools for the Agentic CoT RAG model."""
import json
from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from .connection import vectorstore, chat_model
from .template import summarize_template


# Tool schema
class KeywordsSearchSchema(BaseModel):
    """
    Schema for the "keywords_search" tool.
    """
    keywords: str = Field(
        description=(
            "A list of keywords that are a direct component of the user's request."
        )
    )
    title: str = Field(
        default=None,
        description=(
            "The title of the document in which the search should be performed. "
            "If not provided, the search is performed across the entire corpus for broad search."
        )
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


# Tool implementation
@tool(
    "keywords_search",
    args_schema=KeywordsSearchSchema,
    description=(
        "Search the internal corpus for passages that directly answer a user-defined keyword query. "
        "The function returns the top-k most relevant passages (default 5, maximum 5) along with "
        "complete metadata for each hit. No external data or speculation is included."
    ),
)
def keywords_search(
    keywords: str,
    title: str = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
) -> Command:
    """
    Retrieve the most relevant passages from the internal corpus that directly answer a well-defined keyword query.

    Parameters
    ----------
    keywords : str
        A  list of keywords that are a direct component of the user's request.
        Example: "financial Q1 sales revenue growth"
    title : str | None, optional
        The title of the document in which the search should be performed.
        If not provided, the search is performed across the entire corpus for broad search.

    Returns
    -------
    str
        A markdown-formatted string summarizing the relevant documents found.
    """
    # Build the filter dictionary from the individual parameters
    filter_dict = None
    if title:
        filter_dict = {k: v for k, v in {"title": title}.items() if v.strip()} or None

    # Query
    documents = []
    for keyword in keywords.split(","):
        documents += vectorstore.similarity_search_with_score(keyword, k=10, filter=filter_dict)

    if documents:
        # Sort the results
        documents.sort(key=lambda t: t[1])
        # Return updates
        docs = [{"metadata": doc[0].metadata, "page_content": doc[0].page_content} for doc in documents[:10]]
        sdocs = json.dumps(docs, indent=2, sort_keys=True, ensure_ascii=False)
        # Summarize documents
        formatted_prompt = summarize_template.format(user_query=keywords, documents=sdocs)
        result = chat_model.invoke(formatted_prompt).content
    else:
        result = "I should leave the title field empty."

    # Return updates
    return Command(
        update={
            "messages": [
                ToolMessage(
                    "<think>\n"
                    "```markdown\n"
                    f"{result}\n"
                    "```\n"
                    "</think>",
                    tool_call_id=tool_call_id or "keywords_search",
                )
            ]
        }
    )


