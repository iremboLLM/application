from typing import List, Optional
from pydantic import BaseModel


class FormField(BaseModel):
    label: str
    type: str  # e.g., "text", "email", "number"
    placeholder: Optional[str] = None
    required: bool


class Form(BaseModel):
    title: str
    fields: List[FormField]


class ResponseModel(BaseModel):
    response: str  # The assistant's reply to the user.
    options: Optional[List[str]] = (
        None  # A list of options for the user to choose from.
    )
    tasks: Optional[List[str]] = (
        None  # A list of tasks or steps for the user to follow.
    )
    # form: Optional[Form] = None  # Form details if a form needs to be presented.
    citation: Optional[str] = None  # Cite sources when applicable.
