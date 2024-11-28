"""_summary_

    Returns:
        _type_: _description_
"""

from fastapi import APIRouter

from app.application.services.agent_services import AgentService
from app.infrastructure.ai_engine.agent_runner import AgentRunner
from app.infrastructure.translator.translator import Translator
from app.api.v1.schemas.agent import AgentRequest, AgentResponse

router = APIRouter()
agent_service = AgentService(agent_runner=AgentRunner(), translator=Translator())


@router.post("/agent", response_model=AgentResponse)
async def handle_agent_request(request: AgentRequest):
    """
    Handle an agent request and return the response.

    This endpoint receives a request from an agent, processes it through
    the agent service, and returns the resulting response.

    Args:
    request (AgentRequest): The request object containing the agent's query.
    agent_service (AgentService): The agent service dependency for processing the request.

    Returns:
    dict: A dictionary containing the agent's response.
    """
    # Process the request through the agent service
    result = await agent_service.process_request(request)
    # Return the response as a dictionary
    return result
