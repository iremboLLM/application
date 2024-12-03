"""_summary_

    Returns:
        _type_: _description_
"""

from app.domain.models.agent_response import ResponseModel
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import HumanMessage

from app.domain.models.agent_state import AgentState

from app.infrastructure.ai_engine.prompts.reasoning_prompt import reasoning_prompt

from app.infrastructure.ai_engine.tools.english_retriever import retrieve

from app.infrastructure.ai_engine.tools.apply_for_foreign_document_tool import (
    ApplyForForeignDocumentTool,
)

from app.infrastructure.ai_engine.tools.verify_application_status import (
    verify_application_status_tool,
)

from app.infrastructure.ai_engine.tools.email_application_tool import (
    send_application_document_tool,
)

from app.infrastructure.ai_engine.tools.process_payment import process_payment_tool

from app.config.settings import Settings

app_setting = Settings()


class ReasoningNode:
    """_summary_

    Args:
        Runnable (_type_): _description_
    """

    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: AgentState, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("passenger_id", "12345")
            documents = retrieve(state["messages"][-1].content, 3)

            user_info = passenger_id
            result = self.runnable.invoke(
                {
                    **state,
                    "documents": documents,
                    "user_info": user_info,
                }
            )
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [
                    HumanMessage(content="Respond with a real output.")
                ]
                state = {**state, "messages": messages}
            else:
                break
        return {**state, "messages": result}

    def __str__(self):
        return "SupervisorNode"

    def __repr__(self):
        return "SupervisorNode"


tools = [
    ApplyForForeignDocumentTool,
    verify_application_status_tool,
    process_payment_tool,
    send_application_document_tool,
]
llm = ChatOpenAI(model_name=app_setting.OPENAI_MODEL, temperature=0)
reasoning_node = ReasoningNode(reasoning_prompt | llm.bind_tools(tools=tools))
