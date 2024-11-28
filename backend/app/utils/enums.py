# """
# This module defines enums and configurations for the AI agent.

# It includes an `AgentMode` enum, which represents different modes
# that the AI agent can operate in, such as 'COPILOT', 'DEFAULT', and 'ASSISTANT'.
# """

from enum import Enum


class Language(Enum):
    """
    Enum representing the languages supported by the AI agent.

    Attributes:
        ENGLISH (str): English language.
        FRENCH (str): French language.
        KINYARWANDA (str): Kinyarwanda language.
    """

    ENGLISH = "en"
    FRENCH = "fr"
    KINYARWANDA = "rw"
