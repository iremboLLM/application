"""_summary_

    Returns:
        _type_: _description_
"""

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig
from app.domain.models.agent_state import AgentState

from app.infrastructure.ai_engine.prompts.reasoning_prompt import reasoning_prompt

from app.infrastructure.ai_engine.tools.english_retriever import retrieve

from app.infrastructure.ai_engine.tools.apply_for_foreign_document_tool import (
    ApplyForForeignDocumentTool,
)

# from pydantic import BaseModel, ValidationError

# from langchain_community.tools.tavily_search.tool import TavilySearchResults

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


# class RelevanceResponse(BaseModel):
#     relevant: bool


# def is_relevant(documents, query):
#     """Check if documents are relevant to the user query using an LLM."""
#     if not documents:
#         return RelevanceResponse(relevant=False)

#     # Create the prompt
#     prompt = f"""
# You are a system designed to evaluate the relevance of documents to a given query.

# ### Instructions:
# 1. Assess whether the provided documents are relevant to the user's query.
# 2. A document is **relevant** if it contains information that directly or indirectly addresses the query, or provides context helpful in answering it.
# 3. Provide a structured response in the following JSON format:
#    {{
#        "relevant": <True or False>,
#    }}

# ### Query:
# {query}

# ### Documents:
# {documents}

# Now, evaluate the relevance and provide your response in the specified JSON format.
# """

#     # Send the prompt to the LLM
#     structured_llm = llm.with_structured_output(RelevanceResponse)
#     response = structured_llm.invoke(prompt)

#     # Parse the LLM's response
#     try:
#         # Parse the LLM output as a structured RelevanceResponse
#         return RelevanceResponse(relevant=response.relevant)
#     except ValidationError as e:
#         # Handle invalid or unexpected LLM responses
#         return RelevanceResponse(relevant=False)


# def TavilisySearchRetrieverTool(args: dict) -> str:
#     """
#     __summary
#     """

#     k: int = 10  # Number of top results to return
#     max_results: int = 2
#     # search_depth: str = "advanced"
#     include_answer: bool = True
#     include_raw_content: bool = True
#     include_images: bool = True

#     query = args["query"]
#     # Create a tool call for Tavily search
#     tool_call = {
#         "args": {"query": f"In Rwanda. Always in Rwanda. {query}"},
#         "id": "1",
#         "name": "tavily_search",
#         "type": "tool_call",
#     }

#     print(tool_call)

#     tool = TavilySearchResults(
#         max_results=max_results,
#         # search_depth=search_depth,
#         include_answer=include_answer,
#         include_raw_content=include_raw_content,
#         include_images=include_images,
#         # include_domains=include_domains,
#     )

#     # Use the Tavily search tool to retrieve the search results
#     tool_response = tool.invoke(tool_call)

#     return tool_response


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
            documents = retrieve(state["messages"][-1].content, 1)

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
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {**state, "messages": result}

    def __str__(self):
        return "SupervisorNode"

    def __repr__(self):
        return "SupervisorNode"


tools = [ApplyForForeignDocumentTool]
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
reasoning_node = ReasoningNode(reasoning_prompt | llm.bind_tools(tools=tools))
