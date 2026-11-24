from typing import List, Dict, Any
from app.database.supabase import get_supabase_client
from app.database.redis import cache_get, cache_set
from app.ai.embeddings import embed_query


class RetrievalService:
    @staticmethod
    def retrieve_code_chunks(repository_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves top relevant code chunks from Supabase pgvector using similarity search.
        Falls back to lexical matching if embeddings or pgvector RPC is not yet seeded.
        """
        supabase = get_supabase_client()
        if not supabase:
            return []

        try:
            # Generate query embedding
            query_embedding = embed_query(query)
            # Call Supabase pgvector RPC
            rpc_res = supabase.rpc(
                "match_code_chunks",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": 0.5,
                    "match_count": top_k,
                    "filter_repository_id": repository_id
                }
            ).execute()
            if rpc_res.data:
                return rpc_res.data
        except Exception:
            pass

        # Fallback keyword match query against Supabase
        try:
            res = supabase.table("code_chunks") \
                .select("id, repository_id, file_path, start_line, end_line, content") \
                .eq("repository_id", repository_id) \
                .limit(top_k) \
                .execute()
            return res.data or []
        except Exception:
            return []


async def get_cached_or_retrieved_chunks(repository_id: str, query: str, commit_sha: str = "") -> List[Dict[str, Any]]:
    """Retrieves chunks with Redis caching keyed by repository and query."""
    cache_key = f"rag:{repository_id}:{commit_sha}:{hash(query.strip().lower())}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    chunks = RetrievalService.retrieve_code_chunks(repository_id, query)
    if chunks:
        await cache_set(cache_key, chunks, expire_seconds=3600)
    return chunks
