"""_summary_"""

import os
import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Settings(BaseSettings):
    """
    Configuration class for the FastAPI application.

    This class defines the configuration settings for the FastAPI application.
    It uses the `BaseSettings` class from the `pydantic_settings` library to define the
    settings and their default values.

    Attributes:
        PROJECT_NAME (str): The name of the FastAPI application.
        PROJECT_DESCRIPTION (str): A description of the FastAPI application.
        PROJECT_VERSION (str): The version of the FastAPI application.
    """

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "iremboLLM")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")

    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY", "")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-2")

    MONGO_URL: str = os.getenv("MONGO_URL", "")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
