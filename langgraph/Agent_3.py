import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2,
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    state['messages'].append(AIMessage(content=response.content))
    print("CURRENT STATE: ", state["messages"])
    print(f"AI :  {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []
user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result=agent.invoke({"messages": conversation_history})
    print(result["messages"])
    conversation_history = result["messages"]
    user_input = input("Enter: ")

with open("logging.txt","w",encoding="UTF-8") as f:
    f.write("Your conversation log:\n")
    for messages in conversation_history:
        if isinstance(messages, HumanMessage):
            f.write(f"you: {messages.content}\n")
        elif isinstance(messages, AIMessage):
            f.write(f"AI: {messages.content}\n\n")
    f.write("End of Converstation")

print("conversation saves to logging.txt")