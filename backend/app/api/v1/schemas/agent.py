"""_summary_"""

from typing import Any, List, Optional
from pydantic import BaseModel

from app.domain.models.task_model import TaskExtractionResponse


class AgentRequest(BaseModel):
    """
    A model representing a request made by an agent.

    Attributes:
        query (str): The query string provided by the agent.
    """

    query: str
    agent_mode: Optional[str]
    thread_id: str


class FormField(BaseModel):
    label: str
    type: str  # e.g., "text", "email", "number"
    placeholder: Optional[str] = None
    required: bool


class Form(BaseModel):
    title: Optional[str] = None
    fields: Optional[List[FormField]] = None


class AgentResponse(BaseModel):
    """
    A model representing a response returned by an agent.

    Attributes:
        response (str): The response string returned by the agent.
    """

    response: str
    agent_mode: Optional[str]
    response: str
    text: str
    # form: Optional[Form] = None
    citation: str = ""
    options: list = []
    tasks: list = []
