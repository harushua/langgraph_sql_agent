from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field

class SubmitFinalAnswer(BaseModel):
    """Call this tool to submit the final answer to the user."""
    final_answer: str = Field(..., description="The final answer to the user's question.")

def create_agent_chain(llm: ChatGoogleGenerativeAI, tools: list):
    """
    Creates the agent chain with a specific system prompt and tools.
    """
    query_gen_system = """You are a master SQL expert with a strong attention to detail.
Given an input question and the database schema, write a syntactically correct SQLite query to run.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results to return the most informative samples.
Never query for all columns from a table, only ask for the relevant columns given the question.
If you get an error, or an empty result, rewrite the query and try again.
If you have enough information to answer the question, call the `SubmitFinalAnswer` tool with the answer."""

    prompt = ChatPromptTemplate.from_messages(
        [("system", query_gen_system), ("placeholder", "{messages}")]
    )
    
    # Bind both the SQL tools and the final answer tool
    agent_chain = prompt | llm.bind_tools(tools + [SubmitFinalAnswer])
    return agent_chain