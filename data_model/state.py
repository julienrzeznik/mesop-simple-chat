from dataclasses import dataclass, field
from typing import Literal
from enum import Enum

import mesop as me

from langgraph.graph.graph import CompiledGraph


Role = Literal["user", "model"]

@dataclass(kw_only=True)
class ChatMessage:
    role: Role = "user"
    content: str = ""
    in_progress: bool = False
    rating: int = -1
    comment: str = ""
    run_id: str = ""


@me.stateclass
class State:
    input: str = ""
    messages: list[ChatMessage] = field(default_factory=list)
    email: str = ""
    graph: CompiledGraph = None
    session_id: str = ""
    value: int = 10
