from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.3-70b-versatile")

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

memory = MemorySaver()


class State(TypedDict):
    messages : Annotated[list, add_messages]
    
# Create Some Tools
@tool
def get_stock_price(symbol: str)->float:
    '''Given symbol to stock return current price of Stock'''
    
    return {
        "MSFT": 200.5,
        "AMZN":150.4,
        "MRF":1000.5,
        "RIL": 86.7
    }.get(symbol, 0.0)


@tool 
def buy_stock(symbol: str, quantity:int)->str:
    '''This function will buy stock'''
    curr_price = get_stock_price.invoke({"symbol" : symbol})
    
    total_price = curr_price * quantity
    
    decision = interrupt(
        f"Approve buying {quantity} share of {symbol} for {total_price}"
    )
    
    if decision == "yes":
        return (
            f"Bought {quantity} stocks of {symbol} for {total_price}"
        )
        
    return "Purchased Declined"


tools = [get_stock_price, buy_stock]
llm_with_tool = llm.bind_tools(tools, tool_choice="auto")


def Chatbot(state: State):
    response = llm_with_tool.invoke(
        state['messages']
    )
    
    return {
        "messages": [response]
    }
    
    
builder = StateGraph(State)

builder.add_node("chatbot_node", Chatbot)
builder.add_node("tools", ToolNode(tools))


builder.add_edge(START, "chatbot_node")
builder.add_conditional_edges("chatbot_node", tools_condition)
builder.add_edge("tools", "chatbot_node")

graph = builder.compile(checkpointer=memory)

config1 = {
    "configurable": {
        "thread_id": "1"
    }
}

state = graph.invoke({
    "messages": [{
        'role': 'user',
        'content': 'What is AI? Tell me just full form.'
    }]
}, config=config1)

print(state["messages"][-1].content)

state = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Buy 10 MSFT stocks at current price"
            }
        ]
    },
    config=config1
)

if "__interrupt__" in state:

    print(state["__interrupt__"])

    decision = input("Approve (yes/no): ")

    state = graph.invoke(
        Command(resume=decision),
        config=config1
    )

    print(state["messages"][-1].content)

else:
    print(state["messages"][-1].content)