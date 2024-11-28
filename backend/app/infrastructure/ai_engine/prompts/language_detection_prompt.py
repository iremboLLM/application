"""_summary_"""

from langchain_core.prompts import ChatPromptTemplate

language_detection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful customer support assistant."
            "Your task is to detect the language of the user's query."
            "you should output a JSON object with the following structure:"
            "The only supported languages are English, French and Kinyarwanda."
            "If you do not know the language or you are ensure, use this rule."
            "If there is a Kinyarwanda word, then the language is Kinywarwanda."
            "if you are ensure of the langauge then default the language to english."
            "{{'language': 'en', 'confidence': 0.9}}",
        ),
        ("user", "{messages}"),
    ]
)
