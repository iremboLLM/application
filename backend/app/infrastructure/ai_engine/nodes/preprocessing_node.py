"""_summary_

    Returns:
        _type_: _description_
"""

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig
from app.domain.models.agent_state import AgentState
from app.domain.models.agent_response import ResponseModel

from app.infrastructure.ai_engine.prompts.processing_prompt import processing_prompt

import uuid
from pydantic import BaseModel, Field
from typing import List, Optional


class Task(BaseModel):
    """
    A model representing an individual task.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique Task ID"
    )
    description: str = Field(..., description="Description of the task")
    status: str = Field(
        default="pending", description="Status of the task (default: pending)"
    )


class TaskExtractionResponse(BaseModel):
    """
    A model for the response containing extracted tasks, intent, and goal.
    """

    intent: Optional[str] = Field(
        ..., description="The primary intent of the user's request"
    )
    tasks: Optional[List[Task]] = Field(
        default_factory=list,
        description="List of actionable tasks extracted from the input",
    )
    goal: Optional[str] = Field(
        ..., description="The overarching goal the user wants to achieve"
    )


class TaskExtractionNode:
    """
    A class for processing user input to extract intent, tasks, and a goal.

    Methods:
        extract_tasks(messages: str) -> TaskExtractionResponse:
            Analyzes the input message and returns the extracted data as a Pydantic model.
    """

    @staticmethod
    def extract_tasks(messages: str) -> TaskExtractionResponse:
        """
        Simulates the extraction of intent, tasks, and a goal.

        Args:
            messages (str): The input message from the user.

        Returns:
            TaskExtractionResponse: A Pydantic model containing the extracted data.
        """
        # Simulated extraction logic
        intent = "Help the user obtain a specific document or service."
        tasks = [
            Task(description="Visit the relevant government office or website."),
            Task(description="Fill out the required application form."),
            Task(
                description="Submit necessary documents (e.g., ID, proof of address)."
            ),
            Task(description="Pay any applicable fees."),
        ]
        goal = "Obtain the requested document (e.g., birth certificate)."

        return TaskExtractionResponse(intent=intent, tasks=tasks, goal=goal)


class ProcessingNode:
    """_summary_

    Args:
        Runnable (_type_): _description_
    """

    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: AgentState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state["messages"][-1])
            if not isinstance(result, ResponseModel):
                messages = state["messages"] + [
                    (
                        "user",
                        "Respond with a real output. and ensure you are returning the correct output object",
                    )
                ]
                state = {**state, "messages": messages}
            else:
                return {
                    **state,
                    "should_complete_tasks": False,
                    "tasks": result.tasks if result.tasks else [],
                    # "form": result.form if result.form else None,
                    "options": result.options if result.options else [],
                    "response": result.response if result.response else "",
                    "citation": result.citation if result.citation else "",
                }

    def __str__(self):
        return "SupervisorNode"

    def __repr__(self):
        return "SupervisorNode"


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
llm = llm.with_structured_output(ResponseModel)
processing_node = ProcessingNode(processing_prompt | llm)
