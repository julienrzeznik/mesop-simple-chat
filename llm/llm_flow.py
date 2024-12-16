import os
from uuid import uuid4

import operator
from typing import Annotated, Sequence

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

model = ChatVertexAI(model=os.getenv("MODEL_NAME"), temperature=float(os.getenv("MODEL_TEMPERATURE")), streaming=True)


class GraphState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def agent(state: GraphState):
    system_prompt = f"""You are an assistant. 
    
    Answer the user questions to the best of your knowledge.
    """

    response = model.invoke([SystemMessage(content=system_prompt), *state.messages])
    return {"messages": [response]}


def build_graph():

    graph_builder = StateGraph(GraphState)

    graph_builder.add_node("agent", agent)

    graph_builder.add_edge("agent", END)

    graph_builder.set_entry_point("agent")

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    return graph

chain = build_graph()
