from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from app.ai.llm import get_llm
from app.ai.prompts import (
    QUERY_CLASSIFIER_PROMPT,
    QUERY_REWRITER_PROMPT,
    CONTEXT_EVALUATOR_PROMPT,
    RESPONSE_GENERATOR_PROMPT,
    SOURCE_VERIFIER_PROMPT,
)
from app.schemas.chat import SourceReference


class AgentState(TypedDict):
    query: str
    original_query: str
    query_type: str
    repository_id: str
    retrieved_chunks: List[Dict[str, Any]]
    source_references: List[SourceReference]
    context_text: str
    is_relevant: bool
    retry_count: int
    answer: str


def create_codebase_graph(retriever_func):
    """
    Builds the LangGraph workflow as specified in PRD Section 6.3:
    User Query -> Query Classifier -> Repository Retriever -> Context Relevance Check
      -> If Relevant: Response Generator -> Source Verifier -> Final Answer
      -> If Not Relevant: Query Rewriter -> Repository Retriever (up to bounded retries)
    """

    def query_classifier(state: AgentState) -> Dict[str, Any]:
        llm = get_llm(temperature=0.0)
        chain = QUERY_CLASSIFIER_PROMPT | llm
        res = chain.invoke({"query": state["query"]})
        category = res.content.strip().lower()
        if category not in ["explanation", "debug", "review", "general"]:
            category = "general"
        return {"query_type": category}

    def repository_retriever(state: AgentState) -> Dict[str, Any]:
        repo_id = state["repository_id"]
        q = state["query"]
        chunks = retriever_func(repo_id, q, top_k=5)

        context_lines = []
        refs = []
        for ch in chunks:
            fpath = ch.get("file_path", "unknown")
            sline = ch.get("start_line", 1)
            eline = ch.get("end_line", 1)
            content = ch.get("content", "")
            context_lines.append(f"--- File: {fpath} (Lines {sline}-{eline}) ---\n{content}\n")
            refs.append(SourceReference(
                file_path=fpath,
                start_line=sline,
                end_line=eline,
                snippet=content[:200]
            ))

        return {
            "retrieved_chunks": chunks,
            "source_references": refs,
            "context_text": "\n".join(context_lines)
        }

    def context_relevance_check(state: AgentState) -> Dict[str, Any]:
        chunks = state.get("retrieved_chunks", [])
        if not chunks:
            return {"is_relevant": False}

        llm = get_llm(temperature=0.0)
        chain = CONTEXT_EVALUATOR_PROMPT | llm
        eval_res = chain.invoke({
            "query": state["query"],
            "retrieved_code": state["context_text"][:2500]
        })
        is_rel = "YES" in eval_res.content.upper()
        return {"is_relevant": is_rel}

    def query_rewriter(state: AgentState) -> Dict[str, Any]:
        llm = get_llm(temperature=0.3)
        chain = QUERY_REWRITER_PROMPT | llm
        rewritten = chain.invoke({
            "query": state["query"],
            "context_notes": "Initial retrieval did not match enough specific code symbols."
        })
        return {
            "query": rewritten.content.strip(),
            "retry_count": state.get("retry_count", 0) + 1
        }

    def response_generator(state: AgentState) -> Dict[str, Any]:
        llm = get_llm(temperature=0.2)
        chain = RESPONSE_GENERATOR_PROMPT | llm
        res = chain.invoke({
            "query": state["original_query"],
            "query_type": state["query_type"],
            "context": state["context_text"]
        })
        return {"answer": res.content}

    def source_verifier(state: AgentState) -> Dict[str, Any]:
        evidence_files = [r.file_path for r in state.get("source_references", [])]
        llm = get_llm(temperature=0.0)
        chain = SOURCE_VERIFIER_PROMPT | llm
        verified = chain.invoke({
            "answer": state["answer"],
            "evidence_files": ", ".join(evidence_files)
        })
        return {"answer": verified.content}

    def route_relevance(state: AgentState) -> str:
        if state.get("is_relevant", False):
            return "response_generator"
        if state.get("retry_count", 0) < 1:
            return "query_rewriter"
        return "response_generator"

    workflow = StateGraph(AgentState)
    workflow.add_node("query_classifier", query_classifier)
    workflow.add_node("repository_retriever", repository_retriever)
    workflow.add_node("context_relevance_check", context_relevance_check)
    workflow.add_node("query_rewriter", query_rewriter)
    workflow.add_node("response_generator", response_generator)
    workflow.add_node("source_verifier", source_verifier)

    workflow.set_entry_point("query_classifier")
    workflow.add_edge("query_classifier", "repository_retriever")
    workflow.add_edge("repository_retriever", "context_relevance_check")
    workflow.add_conditional_edges(
        "context_relevance_check",
        route_relevance,
        {
            "response_generator": "response_generator",
            "query_rewriter": "query_rewriter"
        }
    )
    workflow.add_edge("query_rewriter", "repository_retriever")
    workflow.add_edge("response_generator", "source_verifier")
    workflow.add_edge("source_verifier", END)

    return workflow.compile()
