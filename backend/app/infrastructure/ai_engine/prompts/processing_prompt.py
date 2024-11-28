from langchain_core.prompts import ChatPromptTemplate

# Define a concise processing prompt template
processing_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a task extraction assistant. Process user input to identify intent, extract actionable tasks, 
            and define a clear goal based strictly on the input. 

            Guidelines:
            - Return an empty tasks list if no tasks are identified.
            - Summarize the user's intent, extract actionable steps, and define their goal.
            - Use JSON format: {{"intent": "<intent>", "tasks": [{{"id": "<ID>", "description": "<description>", "status": "pending"}}], "goal": "<goal>"}}.
            """,
        ),
        ("user", "{messages}"),
    ]
)
