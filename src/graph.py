from typing import Annotated, Literal, TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from src.agent import create_agent_chain

class State(TypedDict):
    messages: Annotated[list, add_messages]

def build_graph(llm, tools):
    """
    Builds and compiles the agentic graph.
    """
    agent_chain = create_agent_chain(llm, tools)

    # Agent node: The brain of the operation
    def agent_node(state: State):
        print("---NODE: Generating SQL Query---")
        result = agent_chain.invoke(state)
        return {"messages": [result]}

    # Tool node: Executes the tools called by the agent
    tool_node = ToolNode(tools)

    # Router: Decides what to do next
    def should_continue(state: State) -> Literal[END, "tools"]:
        print("---ROUTER: Checking for tool calls---")
        if not state["messages"][-1].tool_calls:
            return END
        return "tools"

    # Assemble the graph
    workflow = StateGraph(State)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
    )
    workflow.add_edge("tools", "agent") # The correction loop
    
    return workflow.compile()