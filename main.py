import os
import time

import mesop as me
import mesop.labs as mel

from uuid import uuid4


from components.standard.header import header
from components.standard.chat_input import chat_input

from pydantic import BaseModel


from components.web.rating.rating_component import (
  rating_component,
)

from data_model.state import State, ChatMessage

from utils.mesop_common import *

from dotenv import load_dotenv


from langfuse import Langfuse

load_dotenv()


if os.getenv("OBSERVE_WITH_LANGFUSE") == "TRUE":
    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST"),
    )


class ParseRating(BaseModel):
  rating: int
  comment: str


def on_send_rating(e: mel.WebEvent):
  # Creating a Pydantic model from the JSON value of the WebEvent
  # to enforce type safety.
    full_rating = ParseRating(**e.value)

    if os.getenv("OBSERVE_WITH_LANGFUSE") == "TRUE":
        langfuse.score(
            trace_id=e.key,
            name="user-explicit-feedback",
            value=full_rating.rating,
            comment=full_rating.comment,
        )

    state = me.state(State)

    for idx, message in enumerate(state.messages):
        if message.run_id == e.key.split("_")[-1]:
            state.messages[idx+1].rating = full_rating.rating
            state.messages[idx+1].comment = full_rating.comment

            break


@me.page(
    path="/",
    stylesheets=STYLESHEETS,
    title="Simple chat",
    security_policy=me.SecurityPolicy(
        dangerously_disable_trusted_types=True,
        allowed_connect_srcs=["*.googleapis.com"],
        allowed_script_srcs=[
            "*.google.com",
            "https://www.gstatic.com",
            "https://cdn.jsdelivr.net",
            "https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js",
        ],
    ),
)
def conversation_page():
    state = me.state(State)

    protect_with_auth = os.getenv("PROTECT_WITH_AUTH")


    with me.box(style=ROOT_BOX_STYLE):

        header(f"### Simple chat")

        if protect_with_auth == "FALSE" or state.email:


            with me.box(
                style=me.Style(
                    width=f"calc(100% - 32px)",
                    gap=16,
                    margin=me.Margin.symmetric(horizontal="auto"),
                    padding=me.Padding.symmetric(horizontal=16),
                )
            ):
                messages = state.messages
                with me.box(
                    style=me.Style(
                        overflow_y="auto",
                    )
                ):

                    for message in messages:
                        if message.role == "user":
                            user_message(message.content)
                        else:
                            model_message(message)

                            rating_component(
                                rating=message.rating,
                                comment=message.comment,
                                key=f"rating_{str(uuid4())}_{message.run_id}",
                                on_send_rating=on_send_rating,
                            )


                    if messages:
                        me.box(
                            key="end_of_messages",
                            style=me.Style(
                                margin=me.Margin(
                                    bottom="50vh" if messages[-1].in_progress else 0
                                )
                            ),
                        )
                with me.box(
                    style=me.Style(
                        display="flex",
                        justify_content="center",
                    )
                ):
                    with me.box(
                        style=me.Style(
                            width="100%",
                            padding=me.Padding(top=24, bottom=24),
                        )
                    ):
                        chat_input()


def user_message(content: str):
    with me.box(
        style=me.Style(
            background="rgb(240, 244, 249)",
            padding=me.Padding.all(16),
            margin=me.Margin.symmetric(vertical=16),
            border_radius=16,
        )
    ):
        me.text(content)


def model_message(message: ChatMessage):
    state = me.state(State)

    with me.box(
        style=me.Style(
            background="#fff",
            padding=me.Padding.all(16),
            border_radius=16,
            margin=me.Margin.symmetric(vertical=16),
        )
    ):

        with me.box(
            style=me.Style(
                margin=me.Margin.symmetric(horizontal="auto"),
                display="flex",
                flex_direction="row",
            )
        ):

            me.markdown(message.content)
            if message.in_progress:
                me.progress_spinner(key=f"spinner_{str(uuid4())}")



