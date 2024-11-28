"""_summary_

    Returns:
        _type_: _description_
"""

import boto3
from langchain_openai import ChatOpenAI
from app.config.settings import Settings

from app.infrastructure.ai_engine.prompts.kinyarwanda_translation_prompt import (
    kinyarwanda_transaltion_prompt,
)

app_settings = Settings()


class Translator:
    """A class to handle text translation using AWS Translate."""

    def __init__(
        self,
        region_name: str = app_settings.AWS_REGION,
        aws_access_key: str = app_settings.AWS_ACCESS_KEY,
        aws_secret_key: str = app_settings.AWS_SECRET_KEY,
    ):
        """
        Initialize the Translator with AWS Translate client.

        Args:
            region_name (str): The AWS region to use.
        """
        self.translate_client = boto3.client(
            service_name="translate",
            region_name=region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    def translate_to_kinyarwanda(self, text: str) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        kinyarwanda_translator = kinyarwanda_transaltion_prompt | llm
        return kinyarwanda_translator.invoke(text)

    def kinyarwanda_to_english(self, text: str) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        return llm.invoke(f"translate this text to english: {text}")

    def translate_text(
        self, text: str, source_language: str, target_language: str = "en"
    ) -> dict:
        """
        Translate text from a source language to a target language.

        Args:
            text (str): The text to translate.
            source_language (str): The source language code (e.g., 'en' for English).
            target_language (str): The target language code (e.g., 'de' for German).

        Returns:
            dict: A dictionary containing the translated text and language codes.
        """
        try:
            if source_language == "rw" and target_language == "en":
                result = self.kinyarwanda_to_english(text)
                return {
                    "TranslatedText": result.content,
                    "SourceLanguageCode": source_language,
                    "TargetLanguageCode": target_language,
                }
            if target_language == "rw":
                result = self.translate_to_kinyarwanda(text)
                return {
                    "TranslatedText": result.content,
                    "SourceLanguageCode": source_language,
                    "TargetLanguageCode": target_language,
                }

            result = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )

            return {
                "TranslatedText": result.get("TranslatedText"),
                "SourceLanguageCode": result.get("SourceLanguageCode"),
                "TargetLanguageCode": result.get("TargetLanguageCode"),
            }
        except Exception as e:
            print(f"Error during translation: {e}")
            return {
                "TranslatedText": None,
                "SourceLanguageCode": source_language,
                "TargetLanguageCode": target_language,
                "Error": str(e),
            }


# Example usage
if __name__ == "__main__":
    translator = Translator(region_name="us-east-2")
    translation_result = translator.translate_text(
        text="Hello, World", source_language="en", target_language="fr"
    )
    print("TranslatedText: ", translation_result.get("TranslatedText", ""))
    print("SourceLanguageCode: ", translation_result.get("SourceLanguageCode", ""))
    print("TargetLanguageCode: ", translation_result.get("TargetLanguageCode", ""))
