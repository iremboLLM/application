"""_summary_

    Returns:
        _type_: _description_
"""

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage

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

            language = state.get("language")

            if language == "en":
                break

            user_message = state["messages"][-1].content
            translated_text = {"TranslatedText": user_message}

            tasks_to_complete = state.get("tasks_to_complete")

            should_complete_tasks = state.get("should_complete_tasks")

            if should_complete_tasks:
                tasks = tasks_to_complete.get("tasks")

                for task in tasks:
                    translated_task = self.translator.translate_text(
                        text=task.description,
                        source_language="en",
                        target_language=language,
                    )
                    task.description = translated_task.get(
                        "TranslatedText", task.description
                    )

                intent = tasks_to_complete.get("intent")
                goal = tasks_to_complete.get("goal")

                translated_intent = self.translator.translate_text(
                    text=intent, source_language="en", target_language=language
                )

                translated_goal = self.translator.translate_text(
                    text=goal, source_language="en", target_language=language
                )

                state = {
                    **state,
                    "should_complete_tasks": True,
                    "tasks_to_complete": {
                        "tasks": tasks,
                        "intent": translated_intent.get("TranslatedText", intent),
                        "goal": translated_goal.get("TranslatedText", goal),
                    },
                }

            # translate to french
            translated_text = self.translator.translate_text(
                text=user_message, source_language="en", target_language=language
            )
            user_message = translated_text.get("TranslatedText", user_message)
            return {
                **state,
                "messages": state["messages"] + [AIMessage(content=user_message)],
            }

        return state

    def __str__(self):
        return "SupervisorNode"

    def __repr__(self):

        return "SupervisorNode"


language_translation_node = LanguageStandarizationNode()
