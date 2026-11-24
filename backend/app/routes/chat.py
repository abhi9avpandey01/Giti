import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationResponse,
    MessageResponse,
    CodeAnalysisRequest
)
from app.database.supabase import get_supabase_client
from app.services.retrieval_service import RetrievalService
from app.ai.graph import create_codebase_graph

router = APIRouter(prefix="/api", tags=["Chat & Code Analysis"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, authorization: Optional[str] = Header(None)):
    """
    Submits a repository-related question to the LangGraph AI RAG workflow.
    """
    supabase = get_supabase_client()
    user_id = "dev-user-00000000-0000-0000-0000-000000000001"

    conv_id = request.conversation_id
    if not conv_id:
        conv_id = str(uuid.uuid4())
        if supabase:
            supabase.table("conversations").insert({
                "id": conv_id,
                "user_id": user_id,
                "repository_id": request.repository_id,
                "title": request.message[:50]
            }).execute()

    # Save user message
    user_msg_id = str(uuid.uuid4())
    if supabase:
        supabase.table("messages").insert({
            "id": user_msg_id,
            "conversation_id": conv_id,
            "role": "user",
            "content": request.message
        }).execute()

    # Compile and invoke LangGraph RAG workflow
    graph = create_codebase_graph(RetrievalService.retrieve_code_chunks)
    initial_state = {
        "query": request.message,
        "original_query": request.message,
        "query_type": "general",
        "repository_id": request.repository_id,
        "retrieved_chunks": [],
        "source_references": [],
        "context_text": "",
        "is_relevant": False,
        "retry_count": 0,
        "answer": ""
    }

    try:
        final_state = graph.invoke(initial_state)
        answer = final_state.get("answer", "Unable to retrieve sufficient context from repository.")
        refs = final_state.get("source_references", [])
        q_type = final_state.get("query_type", "general")
    except Exception as e:
        answer = f"Error during AI reasoning: {str(e)}"
        refs = []
        q_type = "general"

    # Save assistant message
    asst_msg_id = str(uuid.uuid4())
    if supabase:
        supabase.table("messages").insert({
            "id": asst_msg_id,
            "conversation_id": conv_id,
            "role": "assistant",
            "content": answer
        }).execute()

    return ChatResponse(
        conversation_id=conv_id,
        message_id=asst_msg_id,
        answer=answer,
        source_references=refs,
        query_type=q_type
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(authorization: Optional[str] = Header(None)):
    """List conversation histories."""
    supabase = get_supabase_client()
    if not supabase:
        return []
    res = supabase.table("conversations").select("*").order("created_at", desc=True).execute()
    return res.data or []


@router.get("/conversations/{id}", response_model=ConversationResponse)
async def get_conversation(id: str):
    """Get conversation details."""
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=404, detail="Conversation not found")
    res = supabase.table("conversations").select("*").eq("id", id).maybe_single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return res.data


@router.get("/conversations/{id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(id: str):
    """Get all messages for a specific conversation."""
    supabase = get_supabase_client()
    if not supabase:
        return []
    res = supabase.table("messages").select("*").eq("conversation_id", id).order("created_at", desc=False).execute()
    return res.data or []


# Specialized Code Analysis Endpoints (PRD Section 8.4)
@router.post("/repositories/{id}/explain")
async def explain_code(id: str, request: CodeAnalysisRequest):
    """Request code explanation."""
    chat_req = ChatRequest(
        repository_id=id,
        message=f"Explain this code or module: {request.target_path or ''} {request.query or ''} {request.code_snippet or ''}"
    )
    return await chat(chat_req)


@router.post("/repositories/{id}/debug")
async def debug_code(id: str, request: CodeAnalysisRequest):
    """Request bug investigation and troubleshooting."""
    chat_req = ChatRequest(
        repository_id=id,
        message=f"Investigate bug: {request.query or request.code_snippet or 'Analyze possible causes and bugs'}"
    )
    return await chat(chat_req)


@router.post("/repositories/{id}/review")
async def review_code(id: str, request: CodeAnalysisRequest):
    """Request advisory code review."""
    chat_req = ChatRequest(
        repository_id=id,
        message=f"Perform code review on {request.target_path or 'recent files'}: {request.query or 'Check maintainability, security, and bugs'}"
    )
    return await chat(chat_req)
