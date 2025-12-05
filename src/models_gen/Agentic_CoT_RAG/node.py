"""Node definition for the Agentic CoT RAG model."""
from langgraph.prebuilt import create_react_agent
from .state import AgenticCoTRAGState
from .connection import chat_model
from .tool import keywords_search
from .template import systemprompt_template


# Create hook for the ReAct agent.
def react_agent_hook(state: AgenticCoTRAGState) -> AgenticCoTRAGState:
    """
    Hook function to modify the agent state before each action.

    Parameters
    ----------
    state : AgentState
        The current state of the agent.

    Returns
    -------
    AgentState
        The modified state of the agent.
    """
    # Example: Log the current state (this is just a placeholder for actual logic)
    print("Current Agent State:", state)

    # Return the (possibly modified) state
    return state



# Format system prompt
system_prompt = systemprompt_template.format()

# Initialize the ReAct agent with the hook
react_agent = create_react_agent(
    model=chat_model,
    tools=[keywords_search],  # Tools would be added here
    prompt=system_prompt,  # Custom prompt can be added here
    state_schema=AgenticCoTRAGState,
    agent_hook=react_agent_hook,
)
