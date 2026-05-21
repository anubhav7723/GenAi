from dotenv import load_dotenv
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
memory = MemorySaver()

class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def get_stock_price(symbol: str) -> float:
    """Get stock price"""

    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 86.7
    }.get(symbol, 0.0)


@tool
def buy_stock(symbol: str, quantity: int) -> str:
    """Buy stock"""

    current_price = get_stock_price.invoke(
        {"symbol": symbol}
    )

    total_price = current_price * quantity

    decision = interrupt(
        f"Approve buying {quantity} shares of "
        f"{symbol} for {total_price}?"
    )

    if decision == "yes":
        return (
            f"Bought {quantity} shares of "
            f"{symbol} for {total_price}"
        )

    return "Purchase declined"


tools = [get_stock_price, buy_stock]

llm_with_tools = llm.bind_tools(
    tools,
    tool_choice="auto"
)


def chatbot(state: State):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


builder = StateGraph(State)

builder.add_node("chatbot_node", chatbot)

builder.add_node(
    "tools",
    ToolNode(tools)
)

builder.add_edge(
    START,
    "chatbot_node"
)

builder.add_conditional_edges(
    "chatbot_node",
    tools_condition
)

builder.add_edge(
    "tools",
    "chatbot_node"
)

graph = builder.compile(
    checkpointer=memory
)

config = {
    "configurable": {
        "thread_id": "1"
    }
}

# TEST 1
state = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is MSFT stock price?"
            }
        ]
    },
    config=config
)

print(state["messages"][-1].content)

# TEST 2
state = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Buy 10 MSFT stocks at current price"
            }
        ]
    },
    config=config
)

print(state["__interrupt__"])

decision = input("Approve (yes/no): ")

state = graph.invoke(
    Command(resume=decision),
    config=config
)

print(state["messages"][-1].content)