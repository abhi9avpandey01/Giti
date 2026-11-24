from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    repository_id: str = Field(..., description="Target indexed repository UUID")
    conversation_id: Optional[str] = Field(None, description="Existing conversation UUID or None for a new one")
    message: str = Field(..., description="Developer question or instruction")


class SourceReference(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    snippet: Optional[str] = None
    relevance_score: Optional[float] = None


class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    source_references: List[SourceReference] = []
    query_type: Optional[str] = None  # explanation, debug, review, general


class CodeAnalysisRequest(BaseModel):
    target_path: Optional[str] = None
    code_snippet: Optional[str] = None
    query: Optional[str] = None


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    repository_id: str
    title: str
    created_at: Optional[datetime] = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: Optional[datetime] = None
    source_references: Optional[List[SourceReference]] = None
