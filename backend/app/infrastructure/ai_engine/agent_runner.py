"""_summary_

    Returns:
        _type_: _description_
"""

import os
import uuid
from pymongo import MongoClient
from langgraph.graph import StateGraph, START, END

from langgraph.prebuilt import tools_condition

from langchain_core.messages import HumanMessage

from app.utils.agent_mode import AgentMode
from app.domain.models.agent_state import AgentState
from app.infrastructure.ai_engine.nodes.reasoning_node import (
    reasoning_node,
    tools as reasoning_tools,
)

from app.infrastructure.ai_engine.nodes.language_detection_node import (
    language_detection_node,
)
from app.infrastructure.ai_engine.nodes.language_standarization_node import (
    language_standarization_node,
)
from app.infrastructure.ai_engine.nodes.language_translation_node import (
    language_translation_node,
)

from app.infrastructure.ai_engine.nodes.preprocessing_node import processing_node

from app.infrastructure.checkpointer.io import MongoDBSaver
from app.utils.graph_utils import create_tool_node_with_fallback
from app.config.settings import Settings

app_settings = Settings()

# Create a MongoDB client
client = MongoClient(app_settings.MONGO_URL)

checkpointer = MongoDBSaver(
    client=client,
    db_name="iremboLLM",
)


class AgentRunner:
    """Class to configure and run the LangGraph engine."""

    def __init__(self):
        print("=== generating graph ====")
        self.builder = StateGraph(AgentState)

        # self.builder.add_node("language_detection_node", language_detection_node)
        # self.builder.add_node(
        #     "language_standarization_node", language_standarization_node
        # )
        # self.builder.add_node("language_translation_node", language_translation_node)

        # Create and add the SupervisorNode
        self.builder.add_node("reasoning_node", reasoning_node)
        self.builder.add_node(
            "reasoning_tools", create_tool_node_with_fallback(reasoning_tools)
        )

        # self.builder.add_node("preprocessing_node", processing_node)

        self.graph = None
        self.setup_graph()

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def generate_graph(self):
        """
        Save a visual representation of the graph as a PNG file.

        The graph is saved to the specified file path using IPython.display.Image.
        """

        try:
            # Specify the file path where the graph should be saved
            file_path = "graph_representation.png"

            # Generate the graph and save it as a PNG file
            png_data = self.graph.get_graph(xray=True).draw_mermaid_png()
            with open(file_path, "wb") as f:
                f.write(png_data)

            # Optionally, return the file path or a success message
            return f"Graph saved successfully at {os.path.abspath(file_path)}"
        except Exception as e:
            # Handle errors and provide feedback
            return f"Failed to save the graph: {str(e)}"

        # Define the conditional path function

    def setup_graph(self):
        """
        Configure LangGraph to use the agents and tools.

        Sets up the LangGraph engine with nodes and edges.
        """

        # Correctly connect the START node to 'supervisor'
        # self.builder.add_edge(START, "language_detection_node")
        # self.builder.add_edge("language_detection_node", "language_standarization_node")
        # self.builder.add_edge("language_standarization_node", "reasoning_node")
        self.builder.add_edge(START, "reasoning_node")
        self.builder.add_conditional_edges(
            "reasoning_node",
            tools_condition,
            {"tools": "reasoning_tools", "__end__": END},
        )

        self.builder.add_edge("reasoning_tools", "reasoning_node")

        # self.builder.add_edge("reasoning_node", "preprocessing_node")

        self.builder.add_edge("reasoning_node", END)

        # self.builder.add_edge("language_translation_node", END)

        # Compile the graph
        self.graph = self.builder.compile(checkpointer=checkpointer)
        self.generate_graph()
        print(
            "================================= setup completeed =========================================="
        )

    async def run(
        self,
        query: str,
        agent_mode: AgentMode = AgentMode.ASSISTANT.value,
        thread_id: str = str(uuid.uuid4()),
    ) -> AgentState:
        """
        Execute the LangGraph engine with the given state.

        Args:
            state (AgentState): The state object containing the query and messages.

        Returns:
            str: A response string from the Agent runner.
        """
        while self.graph is None:
            await self.setup_graph()
        config = {
            "configurable": {
                # The passenger_id is used in our flight tools to
                # fetch the user's flight information
                "passenger_id": "3442 587242",
                # Checkpoints are accessed by thread_id
                "thread_id": thread_id,
            },
            "recursion_limit": 10,
        }
        # Convert the query to a list of BaseMessages
        state = {
            "messages": ("user", query),
            # "current_mode": agent_mode,
            # "language": HumanMessage(content="en"),
            "language": "en",
        }
        return self.graph.invoke(state, config=config)
        # response = result["messages"][-1].content
