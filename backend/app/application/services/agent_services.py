"""_summary_

    Returns:
        _type_: _description_
"""

from app.infrastructure.ai_engine.agent_runner import AgentRunner
from app.infrastructure.translator.translator import Translator


class AgentService:
    """
    A service class that encapsulates the business logic for the agents.

    This class is responsible for validating the requests made by the agents,
    passing them to the business logic layer, and returning the response to the caller.
    """

    def __init__(self, agent_runner: AgentRunner, translator: Translator):
        """
        Initialize the service with an AgentRunner instance.

        Args:
        agent_runner (AgentRunner): An instance of the AgentRunner class.
        """
        self.agent_runner = agent_runner
        self.translator = translator

    async def process_request(self, request):
        """
        Process a request made by an agent to the system.

        This method is responsible for validating the request, passing it to the
        business logic layer, and returning the response to the caller.

        Args:
        request (AgentRequest): The request object made by the agent.

        Returns:
        AgentResponse: The response object containing the result of the request.
        """
        # Validate the request
        # Business logic goes here
        state = await self.agent_runner(
            request.query, request.agent_mode, request.thread_id
        )

        # print(state["options"])
        # print(state["citation"])
        # print(state["response"])
        # print(state["form"])
        # print(state["tasks"])
        # print(state["messages"])

        # messages = state["messages"]
        # # response = messages[-1].content

        return {
            "agent_mode": request.agent_mode,
            "options": state["options"],
            "citation": state["citation"],
            "response": state["response"],
            # "form": state["form"],
            "tasks": state["tasks"],
            "messages": state["messages"],
            "text": state["messages"][-1].content,
        }
