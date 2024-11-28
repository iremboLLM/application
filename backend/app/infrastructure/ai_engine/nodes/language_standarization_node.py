"""_summary_

    Returns:
        _type_: _description_
"""

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

from app.domain.models.agent_state import AgentState

from app.infrastructure.translator.translator import Translator


class LanguageStandarizationNode:
    """_summary_

    Args:
        Runnable (_type_): _description_
    """

    def __init__(self, translator: Translator = Translator()):
        """
        Initialize the AssistantNode with a Runnable instance.

        Args:
            runnable (Runnable): The Runnable instance to use in the node.
        """
        self.translator = translator

    def __call__(self, state: AgentState, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("passenger_id", "12345")
            state = {**state, "user_info": passenger_id}

            user_message = state["messages"][-1].content
            translated_text = {"TranslatedText": user_message}

            language = state.get("language")
            if language == "en":
                break
            else:
                # translate to french
                translated_text = self.translator.translate_text(
                    text=user_message, source_language=language, target_language="en"
                )
                user_message = translated_text.get("TranslatedText", user_message)
                return {
                    **state,
                    "messages": state["messages"]
                    + [HumanMessage(content=user_message)],
                }
        return state

    def __str__(self):
        return "SupervisorNode"

    def __repr__(self):
        return "SupervisorNode"


language_standarization_node = LanguageStandarizationNode()
