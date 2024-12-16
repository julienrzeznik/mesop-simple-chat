import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.runnables import Runnable


from langfuse import Langfuse

load_dotenv()

if os.getenv("OBSERVE_WITH_LANGFUSE") == "TRUE":
  langfuse = Langfuse(
      public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
      secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
      host=os.getenv("LANGFUSE_HOST"),
  )

def pydantic_to_dict(obj):
  """
  Recursively converts a dictionary containing Pydantic models 
  into a pure dictionary.

  Args:
    obj: The dictionary potentially containing Pydantic models.

  Returns:
    A pure dictionary with no Pydantic models.
  """

  if isinstance(obj, dict):
    return {key: pydantic_to_dict(value) for key, value in obj.items()}
  elif isinstance(obj, BaseModel):
    return obj.dict()
  elif isinstance(obj, list):
    return [pydantic_to_dict(item) for item in obj]
  else:
    return obj




async def stream_from_chain(chain: Runnable, session_id: str, run_id: str, graph_state: dict) -> AsyncGenerator[str, None]:
    
    try:

        callbacks = []

        if os.getenv("OBSERVE_WITH_LANGFUSE") == "TRUE":
          trace = langfuse.trace(id=run_id, session_id=session_id)
          langfuse_handler_trace = trace.get_langchain_handler(
              update_parent=True # add i/o to trace itself as well
          )
          callbacks = [langfuse_handler_trace]


        # Generate a new conversation ID
        config = {"configurable": {"thread_id": session_id} , "callbacks":callbacks, "run_name": run_id}

        async for data in chain.astream_events(graph_state, stream_mode=["values", "messages"], config=config, version="v2"):
            yield pydantic_to_dict(data)
        
    except Exception as e:
        yield f"Exception. {e}"


