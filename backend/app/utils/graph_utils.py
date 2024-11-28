"""_summary_

    Returns:
        _type_: _description_
"""

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda

from langgraph.prebuilt import ToolNode

from app.domain.models.agent_state import AgentState


def handle_tool_error(state: dict) -> AgentState:
    """
    This function handles errors from tool calls.

    When an error occurs from a tool call, this function is called with the current
    state. It will add a new message to the state with the error message and the
    tool call that caused the error.

    Args:
        state (dict): The current state of the conversation.

    Returns:
        dict: The updated state with the new error message.
    """
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    state["messages"].extend(
        [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    )
    return state


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)
