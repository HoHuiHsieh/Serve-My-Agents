"""Configures the state graph for the Agentic CoT RAG model generator."""
from langgraph.graph import StateGraph, END
from .node import react_agent
from .state import AgenticCoTRAGState


workflow = StateGraph(AgenticCoTRAGState)
workflow.add_agent(react_agent, "react_agent")
workflow.set_entry_point("react_agent")
workflow.add_edge("react_agent", END)
graph = workflow.compile()