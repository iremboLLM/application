import os
from supabase import create_client, Client
from app.config.settings import Settings

app_settings = Settings()


class SupabaseClient:
    """Class to handle connections and queries with Supabase."""

    def __init__(
        self, url: str = app_settings.SUPABASE_URL, key: str = app_settings.SUPABASE_KEY
    ):
        # Load environment variables for Supabase URL and Key
        self.url = url
        self.key = key

        if not self.url or not self.key:
            raise ValueError(
                "Supabase URL and Key must be set in environment variables."
            )

        # Create a Supabase client
        self.client: Client = create_client(self.url, self.key)
        print("===== successfully connected to supabase ====")

    def insert_embedding(self, table_name: str, data: dict):
        """
        Inserts an embedding into the specified table.

        Args:
            table_name (str): The name of the table to insert into.
            data (dict): The data to insert (e.g., {"embedding": [0.1, 0.2, 0.3], "text": "example"}).

        Returns:
            dict: The response from Supabase.
        """
        response = self.client.table(table_name).insert(data).execute()
        if response.error:
            raise Exception(f"Error inserting data: {response.error}")
        return response.data

    def query_embeddings(self, table_name: str, filters: dict):
        """
        Queries embeddings from the specified table based on filters.

        Args:
            table_name (str): The name of the table to query from.
            filters (dict): A dictionary of filters (e.g., {"text": "example"}).

        Returns:
            list: A list of results matching the filters.
        """
        query = self.client.table(table_name).select("*")
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        if response.error:
            raise Exception(f"Error querying data: {response.error}")
        return response.data

    def delete_embedding(self, table_name: str, condition: dict):
        """
        Deletes an embedding from the specified table based on a condition.

        Args:
            table_name (str): The name of the table to delete from.
            condition (dict): The condition for deletion (e.g., {"id": 1}).

        Returns:
            dict: The response from Supabase.
        """
        query = self.client.table(table_name).delete()
        for key, value in condition.items():
            query = query.eq(key, value)
        response = query.execute()
        if response.error:
            raise Exception(f"Error deleting data: {response.error}")
        return response.data


supabase_client = SupabaseClient()
