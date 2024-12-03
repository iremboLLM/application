"""
This script processes PDF files in the 'docs' folder, extracts their text content, and stores them
in an in-memory Chroma vector store for efficient document retrieval. It uses the PyMuPDF library to
extract text from PDFs, Langchain's OpenAI embeddings for vector representation, and Chroma for
storing the vectors and performing similarity searches.

Functions:
- extract_text_from_pdf: Extracts text from a given PDF file asynchronously.
- create_vector_store: Creates an in-memory Chroma vector store by processing all PDFs in the 'docs' folder.
- retrieve: Retrieves relevant documents from the vector store based on a query.
"""

import os
from uuid import uuid4
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter


# Folder containing the PDFs
DOCS_FOLDER = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "docs", "english"
)
# Initialize Chroma client and embeddings
embeddings = OpenAIEmbeddings()
vector_store = Chroma(
    collection_name="english",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

# Initialize the text splitter (split by 1000 characters, modify as needed)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        List[str]: A list of extracted pages' text.
    """
    loader = PyPDFLoader(pdf_path)
    pages = []
    for page in loader.lazy_load():
        pages.append(page)
    return pages


def create_vector_store() -> Chroma:
    """
    Create an in-memory Chroma vector store with the extracted documents.

    This function collects all PDFs in the 'docs' folder, extracts their text
    using PyMuPDF, splits the text using the text splitter, and creates an in-memory Chroma vector store
    with the extracted documents.

    Returns:
        Chroma: The in-memory Chroma vector store.
    """
    # Check if vector store already contains data
    if vector_store._collection.count() > 0:
        print("Vector store already contains data. Skipping processing.")
        return vector_store

    documents = []
    metadata = []

    # Collect all PDFs in the 'docs' folder
    for filename in os.listdir(DOCS_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DOCS_FOLDER, filename)
            print(f"Processing file: {filename}")

            # Extract text from the PDF using PyMuPDF
            doc = extract_text_from_pdf(pdf_path)

            # Append the split text and metadata to the lists
            documents.extend(doc)
            metadata.extend([{"source": filename}] * len(doc))

    # Ensure documents are not empty before adding to the vector store
    if not documents:
        raise ValueError("No documents found to add to the vector store.")

    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Added {len(documents)} documents to the vector store.")

    return vector_store


create_vector_store()


def retrieve(query: str, num_results: int = 5) -> List[dict]:
    """
    Retrieve relevant documents from the vector store based on the query.

    Args:
        query (str): The query to search for.
        num_results (int): The number of documents to retrieve.

    Returns:
        List[dict]: A list of relevant documents from the vector store.
    """
    results = vector_store.similarity_search(query, k=num_results)
    return results


# Main entry point
if __name__ == "__main__":
    QUERY = "What is the process of applying for services?"

    print(retrieve(QUERY))
