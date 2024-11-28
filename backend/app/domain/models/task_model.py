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
