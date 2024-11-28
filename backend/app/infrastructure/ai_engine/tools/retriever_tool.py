"""_summary_

Returns:
    _type_: _description_
"""

from typing import List

from langsmith import traceable

from langchain_core.documents import Document

from langchain_openai import OpenAIEmbeddings

from supabase import create_client, Client
from langchain.agents import Tool

from app.config.settings import Settings

app_setting = Settings()

# Initialize Supabase client
supabase_url = app_setting.SUPABASE_URL
supabase_key = app_setting.SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)


@traceable(
    run_type="retriever",
    name="retrieve_irembo_faqs_docs",
    tags=["conversation", "faqs", "retrieval"],
    metadata={"version": "1.0", "author": "IremboLLM-APP"},
)
def retrieve_documents_tool(query: str) -> List[Document]:
    """
    Retrieves the top-k documents from the Supabase database that match the given query.

    Args:
    - query (str): The query to search for.
    - document_type_id (str): The ID of the document type to search in.
    - top_k (int, optional): The number of documents to retrieve. Defaults to 5.

    Returns:
        List[Document]: A list of the top-k matching documents.
    """
    document_type_id: str = "irembo_faqs"
    top_k: int = 2
    threshold: float = 0.75
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Create embedding for the query
    query_embedding = embeddings.embed_query(query)

    # Perform the RPC call to Supabase to retrieve the top-k matching documents
    results = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "filter": {"document_type_id": document_type_id},
            "match_count": top_k,
        },
    ).execute()

    # Process and return results
    documents = []
    for doc in results.data:
        documents.append(
            Document(
                page_content=doc["content"],
                metadata={
                    "relevance": doc["similarity"],  # Use similarity score as relevance
                    "source": doc["document_type_id"],
                    "score": doc["similarity"],
                    "document_type_id": doc["document_type_id"],
                    "id": doc["id"],
                },
            )
        )

    # Sort documents by score
    documents = sorted(documents, key=lambda d: d.metadata["score"], reverse=True)
    # documents = filter(lambda d: d.score > threshold, documents)
    return documents


RetrieveDocumentsTool = Tool(
    name="retrieve_irembo_faqs_docs",
    description="""Primary tool for retrieving FAQ-based information on Irembo services such as motor vehicle inspection, certificate of being single, and foreign travel documents. Use this resource to provide users with detailed service descriptions, application steps, and answers to frequently asked questions.""",
    func=retrieve_documents_tool,
)
