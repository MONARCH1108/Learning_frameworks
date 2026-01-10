from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
    """add the two values a + b"""
    return a + b

@tool
def multiply(a: int, b: int):
    """ multiple the two numbers"""
    return a * b

@tool
def subtract(a: int, b: int):
    """ subtract the two numbers"""
    return a - b

@tool
def divide(a: int, b: int):
    """ subtract the two numbers"""
    return a / b

tools = [add, subtract, multiply, divide]

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",   
    temperature=0.2,
).bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="your name is jarvis and you are my best friend"
    )
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if not getattr(last_message, "tool_calls", None):
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent", should_continue,
    {
        "continue": "tools",
        "end": END,
    }
)
graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1] 
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [HumanMessage(content="add 344+4345. add 3+4 , 344+4345/12345,  ")]}
print_stream(app.stream(inputs, stream_mode="values"))
