
import mesop as me

from uuid import uuid4

from data_model.state import State, ChatMessage

from llm.llm_flow import chain
from llm.stream_local import stream_from_chain

from langchain_core.messages import HumanMessage


def chat_input():
    state = me.state(State)
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):

        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                key="key_chat_input",
                value=state.input,
                placeholder="Enter a prompt",
                shortcuts={
                    me.Shortcut(key="enter"): on_submit, 
                },
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    height="100px",
                    border=me.Border.all(me.BorderSide(style="none")),
                    background="rgb(240, 244, 249)",
                    border_radius=16,
                ),
            )



async def on_submit(e: me.TextareaShortcutEvent):
    state = me.state(State)
    
    # If there are no messages yet, initialize
    if not state.messages:
        state.messages=[]
        state.session_id = str(uuid4())
    
    state.input = e.value
    input = state.input

    yield
    
    state.input = ""
    yield
    
    # Get the messages
    messages = state.messages
    history = messages[:]
    
    run_id = str(uuid4())

    # Add a new message with the user content
    messages.append(ChatMessage(role="user", content=input, run_id=run_id))
    
    new_message = ChatMessage(role="model", in_progress=True, run_id=run_id)

    # Add a new message with the model response (that will be filled in streaming)
    messages.append(new_message)
    
    yield
    
    # Scroll to the end of the messages
    me.scroll_into_view(key="end_of_messages")
    
    graph_state = {"messages": [HumanMessage(content=input)]}

    stream = stream_from_chain(chain, state.session_id, run_id, graph_state)
    
    async for event in stream:
        event_type = str(event.get("event"))
        if event_type == 'on_chat_model_stream':
            content = event["data"]["chunk"]["content"]
            new_message.content += content
            yield
    
    # Remove the in_progress flag
    new_message.in_progress = False
    yield





