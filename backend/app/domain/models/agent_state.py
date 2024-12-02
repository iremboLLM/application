"""_summary_

    Returns:
        _type_: _description_
"""

from typing import Annotated, Dict, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """_summary_"""

    messages: Annotated[list, add_messages]
    # current_mode: Annotated[list, add_messages]  # Custom handler
    language: str
    should_complete_tasks: Optional[bool]
    tasks_to_complete: Optional[Dict[str, Optional[any]]]
    tasks: list
    form: any
    citation: str
    options: list
    response: str
