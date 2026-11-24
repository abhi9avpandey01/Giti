from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings


def get_llm(temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """Returns configured Google Gemini Chat model instance."""
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        convert_system_message_to_human=True,
    )
