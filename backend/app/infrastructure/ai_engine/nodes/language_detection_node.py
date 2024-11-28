"""_summary_

    Returns:
        _type_: _description_
"""

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field

from app.domain.models.agent_state import AgentState
from app.infrastructure.ai_engine.prompts.language_detection_prompt import (
    language_detection_prompt,
)


# Define the GoalEvaluationOutput model
class LanguageDetectionOutput(BaseModel):
    """
    A model representing the output of language detection.

    Attributes:
        language (str): The language of the user input, with possible values:
            - 'rw' for Kinyarwanda
            - 'fr' for French
            - 'en' for English
        confidence (str): The confidence level of the language detection.
    """

    language: str = Field(
        description="The language of the user input either rw for kinyarwanda, fr for french and en for english",
        default="en",
    )
    confidence: str = Field(
        description="The confidence level of the language detection", default="0.9"
    )


class LanguageDetectionNode:
    """_summary_

    Args:
        Runnable (_type_): _description_
    """

    def __init__(self, runnable: Runnable):
        """
        Initialize the AssistantNode with a Runnable instance.

        Args:
            runnable (Runnable): The Runnable instance to use in the node.
        """
        self.runnable = runnable

    def __call__(self, state: AgentState, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("passenger_id", "12345")
            state = {**state, "user_info": passenger_id}
            result = self.runnable.invoke(state["messages"][-1].content)
            if isinstance(result, LanguageDetectionOutput):
                break
            else:
                messages = state["messages"] + [
                    ("user", "Please detect a valid language between rw, fr and en.")
                ]
                state = {**state, "messages": messages}

        return {**state, "language": result.language}

    def __str__(self):
        return "SupervisorNode"

    def __repr__(self):
        return "SupervisorNode"


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
llm = llm.with_structured_output(LanguageDetectionOutput)
language_detection_node = LanguageDetectionNode(language_detection_prompt | llm)
