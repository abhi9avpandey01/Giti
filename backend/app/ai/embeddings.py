from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings


def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    """Returns Google Gemini Embeddings model instance."""
    return GoogleGenerativeAIEmbeddings(
        model=settings.GEMINI_EMBEDDING_MODEL,
        google_api_key=settings.GEMINI_API_KEY
    )


def embed_query(query: str) -> List[float]:
    """Generates embedding for a single text query."""
    model = get_embeddings_model()
    return model.embed_query(query)


def embed_documents(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a batch of code chunks."""
    model = get_embeddings_model()
    return model.embed_documents(texts)
