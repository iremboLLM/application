"""_summary_

Returns:
    _type_: _description_
"""

from uuid import uuid4

from typing import List

from langsmith import traceable

from langchain_core.documents import Document

from langchain_openai import OpenAIEmbeddings
from typing import Annotated

from pydantic import BaseModel
from supabase import create_client, Client

# from langchain.agents import StructuredTool
from langchain_core.tools import StructuredTool

from app.config.settings import Settings

app_setting = Settings()

# Initialize Supabase client
supabase_url = app_setting.SUPABASE_URL
supabase_key = app_setting.SUPABASE_KEY
# supabase: Client = create_client(supabase_url, supabase_key)
# Supabase client setup
supabase: Client = create_client(
    supabase_key=supabase_key,
    supabase_url=supabase_url,
)


def apply_for_foreign_document_tool(
    first_name: str,
    last_name: str,
    passport_number: str = "012345",
    type_of_travel_document: str = "emergency travel documents",
    # args: dict,
) -> List[Document]:
    """
    Inserts data into the Supabase Foreign_Travel table for a specified travel document type.

    Args:
        first_name (str): First name of the applicant.
        last_name (str): Last name of the applicant.
        passport_number (str, optional): Passport number of the applicant. Defaults to "012345".
        type_of_travel_document (str, optional): Type of travel document to insert. Defaults to "document".

    Returns:
        List[Document]: A list of Document objects representing the data inserted or error details.
    """
    print("i am hereeeeee ==========================================")
    ID = str(uuid4())

    print("============== id ==============\n", ID)

    if first_name is None or last_name is None:
        print("First name and last name must be provided.")
        raise ValueError("First name and last name must be provided.")
    try:
        # Insert data into Supabase table with validated type
        data, error = (
            supabase.from_("Foreign_Travel")
            .insert(
                [
                    {
                        "Surname": first_name.lower(),
                        "otherName": last_name.lower(),
                        "Passportnumber": passport_number.lower(),
                        "type_of_travel_document": type_of_travel_document.lower(),
                        "user_id": f"user_id_{ID}",
                        "status": "awaiting_payment",
                        "billing_id": ID,
                    }
                ]
            )
            .execute()
        )

        print("============== error ================\n", data, error)

        # Check if error is a tuple and if it contains a non-None error
        if isinstance(error, tuple) and error[1] is not None:
            return f"Error inserting data: {error}"
        elif data:
            return f"Data inserted successfully: {data}"
        else:
            return "Unexpected response: No data returned, and no error detected."

    except Exception as e:
        print("The error ===================", e)
        return f"Exception: {str(e)}"


# Define the Pydantic model for the input arguments
class ApplyForForeignDocumentArgs(BaseModel):
    first_name: str
    last_name: str
    passport_number: str = "012345"
    type_of_travel_document: str = "document"


ApplyForForeignDocumentTool = StructuredTool(
    name="apply_for_foreign_document_tool",
    description=(
        "This tool inserts data into the Supabase 'Foreign_Travel' table for foreign travel document services. "
        "Provide a the following: "
        "- `first_name` (str): The first name of the applicant. "
        "- `last_name` (str): The last name of the applicant. "
        "- `passport_number` (str, optional): The passport number of the applicant. Defaults to '012345'. "
        "- `type_of_travel_document` (str, optional): The type of travel document, which can be 'document' or 'passport'. "
        "Defaults to 'document'."
    ),
    func=apply_for_foreign_document_tool,
    args_schema=ApplyForForeignDocumentArgs,
)
