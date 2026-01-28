import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Define state
class AgentState(TypedDict):
    user_input: str
    response: str

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
)

def agent_node(state: AgentState):
    result = llm.invoke(state["user_input"])
    return {"response": result.content}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

agent_app = graph.compile()
