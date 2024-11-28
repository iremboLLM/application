"""
This module defines enums and configurations for the AI agent.

It includes an `AgentMode` enum, which represents different modes
that the AI agent can operate in, such as 'COPILOT', 'DEFAULT', and 'ASSISTANT'.
"""

from enum import Enum


class AgentMode(Enum):
    """
    Enum representing the different modes of the AI agent.

    Modes:
        - COPILOT: The AI agent is in copilot mode, assisting the user in generating code based on human instructions.
        - DEFAULT: The AI agent is in default mode, generating code without any additional instructions from the user.
        - ASSISTANT: The AI agent is in assistant mode, available to provide more general assistance.
    """

    COPILOT = "copilot"
    DEFAULT = "default"
    ASSISTANT = "assistant"


if __name__ == "__main__":
    print(AgentMode.COPILOT.value)
    print(AgentMode.DEFAULT.value)
    print(AgentMode.ASSISTANT.value)
