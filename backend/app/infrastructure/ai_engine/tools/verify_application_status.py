"""
Summary:
This module provides tools and functions for managing foreign travel document applications.
It includes a tool to insert data into the Supabase 'Foreign_Travel' table and to verify the application status.

Classes:
    ApplyForForeignDocumentArgs: Pydantic model for foreign document application arguments.

Functions:
    verify_application_status: Verifies the application status for a given billing ID.
    apply_for_foreign_document_tool: Handles the insertion of foreign document application data into Supabase.

Returns:
    StructuredTool: A tool for managing foreign travel document applications.
"""

from typing import List
from langchain_core.documents import Document
from pydantic import BaseModel
from supabase import create_client, Client
from langchain_core.tools import StructuredTool
from app.config.settings import Settings

# Load application settings
app_setting = Settings()

# Initialize Supabase client
supabase_url = app_setting.SUPABASE_URL
supabase_key = app_setting.SUPABASE_KEY
supabase: Client = create_client(
    supabase_key=supabase_key,
    supabase_url=supabase_url,
)


def verify_application_status(billing_id: str) -> List[Document]:
    """
    Verifies the application status for a foreign travel document based on the given billing ID.

    Args:
        billing_id (str): The billing ID associated with the application.

    Returns:
        List[Document]: A list of documents containing the application details, or a string message if an error occurs.

    Raises:
        ValueError: If billing_id is not provided.
    """
    if not billing_id:
        raise ValueError("billing_id must be provided.")

    try:
        data, error = (
            supabase.table("Foreign_Travel")
            .select("*")
            .eq("billing_id", billing_id)
            .execute()
        )

        # Handle potential errors
        if isinstance(error, tuple) and error[1] is not None:
            return f"Error fetching data: {error}"
        elif data:
            return f"Application details: {data}"
        else:
            return "Unexpected response: No data returned, and no error detected."

    except Exception as e:
        return f"Exception: {str(e)}"


class VerifyApplicationStatusArgs(BaseModel):
    """
    Pydantic model for foreign travel document application arguments.

    Attributes:
        billing_id (str): The billing ID for the application.
    """

    billing_id: str


verify_application_status_tool = StructuredTool(
    name="verify_application_status_tool",
    description=(
        "This tool is used to verify the application status for a foreign travel document. "
        "Provide the following details: "
        "- `billing_id` (str): The billing ID associated with the application. "
    ),
    func=verify_application_status,
    args_schema=VerifyApplicationStatusArgs,
)
