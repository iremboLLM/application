"""
Summary:
This module provides tools and functions for managing payments for foreign travel document applications.
It includes a tool to process payments using a credit card and billing ID.

Classes:
    ProcessPaymentArgs: Pydantic model for payment processing arguments.

Functions:
    process_payment: Processes the payment and updates the application status.

Returns:
    StructuredTool: A tool for handling payments for foreign travel document applications.
"""

from typing import List
from pydantic import BaseModel, Field
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


def process_payment(billing_id: str, credit_card: str) -> str:
    """
    Processes the payment for a foreign travel document application and updates its status.

    Args:
        billing_id (str): The billing ID associated with the application.
        credit_card (str): The credit card number for the payment.

    Returns:
        str: A success message or an error message if the process fails.

    Raises:
        ValueError: If billing_id or credit_card is not provided.
    """
    if not billing_id:
        raise ValueError("billing_id must be provided.")
    if not credit_card:
        raise ValueError("credit_card must be provided.")

    try:
        # Simulate payment processing (replace this with actual payment gateway integration)
        print(
            f"Processing payment for billing_id: {billing_id} using credit_card: {credit_card}"
        )

        old_data = (
            supabase.table("Foreign_Travel")
            .select("*")
            .eq("billing_id", billing_id)
            .execute()
            .data
        )
        if not old_data:
            return f"Error: No data found for billing_id: {billing_id}"

        if old_data[0]["status"] != "awaiting_payment":
            return f"Error: Payment already processed for billing_id: {billing_id}"

        # Payment successful, update the status in the database
        data, error = (
            supabase.table("Foreign_Travel")
            .update({"status": "pending"})
            .eq("billing_id", billing_id)
            .execute()
        )

        # Handle potential errors
        if isinstance(error, tuple) and error[1] is not None:
            return f"Error updating status: {error}"
        elif data:
            return "Payment processed successfully. Application status updated to 'pending'."
        else:
            return "Unexpected response: Payment processed, but status update failed."

    except Exception as e:
        return f"Exception: {str(e)}"


class ProcessPaymentArgs(BaseModel):
    """
    Pydantic model for payment processing arguments.

    Attributes:
        billing_id (str): The billing ID for the application.
        credit_card (str): The credit card number for payment.
    """

    billing_id: str = Field(..., description="The billing ID for the application.")
    credit_card: str = Field(..., description="The credit card number for payment.")


process_payment_tool = StructuredTool(
    name="process_payment_tool",
    description=(
        "This tool is used to process payments for foreign travel document applications. "
        "Provide the following details: "
        "- `billing_id` (str): The billing ID associated with the application. "
        "- `credit_card` (str): The credit card number for payment. "
        "After payment is processed, the application status will be updated to 'pending'."
    ),
    func=process_payment,
    args_schema=ProcessPaymentArgs,
)
