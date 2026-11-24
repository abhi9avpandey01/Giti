import uuid
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.github_service import GitHubService
from app.ai.embeddings import embed_documents
from app.database.supabase import get_supabase_client
from app.database.redis import cache_set


class IndexingService:
    def __init__(self, github_service: GitHubService = None):
        self.github_service = github_service or GitHubService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=["\ndef ", "\nclass ", "\nfunction ", "\nexport ", "\n\n", "\n", " "]
        )

    def chunk_source_code(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Splits source code into chunks preserving approximate line numbers."""
        lines = content.splitlines(keepends=True)
        chunks = []
        raw_chunks = self.text_splitter.split_text(content)

        current_line = 1
        for chunk_text in raw_chunks:
            chunk_line_count = len(chunk_text.splitlines())
            start_line = current_line
            end_line = start_line + max(1, chunk_line_count) - 1

            chunks.append({
                "file_path": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "content": chunk_text
            })
            # Advance approximate line counter
            current_line = max(start_line + 1, end_line - 2)

        return chunks

    async def index_repository(self, repository_id: str, github_url: str, branch: str = "main") -> Dict[str, Any]:
        """Orchestrates repository indexing workflow."""
        owner, repo = self.github_service.parse_repo_url(github_url)
        supabase = get_supabase_client()

        # Update status in Redis and Supabase
        await cache_set(f"indexing_status:{repository_id}", "indexing", expire_seconds=1800)
        if supabase:
            supabase.table("repositories").update({"indexing_status": "indexing"}).eq("id", repository_id).execute()

        try:
            commit_sha = await self.github_service.get_latest_commit_sha(owner, repo, branch)
            tree_files = await self.github_service.fetch_repository_tree(owner, repo, commit_sha)

            all_chunks = []
            # Index up to 50 key files for fast, simple, responsive initial ingestion
            for file_item in tree_files[:50]:
                path = file_item["path"]
                sha = file_item["sha"]
                try:
                    file_content = await self.github_service.fetch_file_content(owner, repo, sha)
                    file_chunks = self.chunk_source_code(path, file_content)
                    for fc in file_chunks:
                        fc["repository_id"] = repository_id
                        all_chunks.append(fc)
                except Exception:
                    continue

            # Generate embeddings and store in pgvector
            if all_chunks:
                texts = [c["content"] for c in all_chunks]
                try:
                    embeddings = embed_documents(texts)
                    for c, emb in zip(all_chunks, embeddings):
                        c["embedding"] = emb
                except Exception:
                    # Proceed without embeddings if API key is unconfigured in dev
                    pass

                if supabase:
                    # Clear previous chunks for repository if re-indexing
                    supabase.table("code_chunks").delete().eq("repository_id", repository_id).execute()
                    # Insert in batches
                    batch_size = 50
                    for i in range(0, len(all_chunks), batch_size):
                        batch = all_chunks[i:i + batch_size]
                        supabase.table("code_chunks").insert(batch).execute()

            # Mark completed
            if supabase:
                supabase.table("repositories").update({
                    "commit_sha": commit_sha,
                    "indexing_status": "completed"
                }).eq("id", repository_id).execute()

            await cache_set(f"indexing_status:{repository_id}", "completed", expire_seconds=86400)
            return {
                "repository_id": repository_id,
                "commit_sha": commit_sha,
                "indexed_files": len(tree_files),
                "chunks_count": len(all_chunks),
                "status": "completed"
            }

        except Exception as e:
            if supabase:
                supabase.table("repositories").update({"indexing_status": "failed"}).eq("id", repository_id).execute()
            await cache_set(f"indexing_status:{repository_id}", "failed", expire_seconds=3600)
            raise e
