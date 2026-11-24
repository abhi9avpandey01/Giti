import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Header
from app.schemas.repository import RepositoryConnectRequest, RepositoryResponse
from app.database.supabase import get_supabase_client
from app.services.github_service import GitHubService
from app.services.indexing_service import IndexingService

router = APIRouter(prefix="/api/repositories", tags=["Repositories"])


def get_user_id(authorization: Optional[str]) -> str:
    # Helper to resolve user id
    return "dev-user-00000000-0000-0000-0000-000000000001"


@router.get("", response_model=List[RepositoryResponse])
async def list_repositories(authorization: Optional[str] = Header(None)):
    """List all connected repositories for user."""
    user_id = get_user_id(authorization)
    supabase = get_supabase_client()
    if not supabase:
        return []

    res = supabase.table("repositories").select("*").eq("user_id", user_id).execute()
    return res.data or []


@router.post("/connect", response_model=RepositoryResponse)
async def connect_repository(
    payload: RepositoryConnectRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    """Connect a GitHub repository and initiate indexing."""
    user_id = get_user_id(authorization)
    github_service = GitHubService()
    try:
        owner, repo_name = github_service.parse_repo_url(payload.github_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    repo_id = str(uuid.uuid4())
    repo_data = {
        "id": repo_id,
        "user_id": user_id,
        "github_url": payload.github_url,
        "name": f"{owner}/{repo_name}",
        "branch": payload.branch or "main",
        "indexing_status": "pending"
    }

    supabase = get_supabase_client()
    if supabase:
        supabase.table("repositories").insert(repo_data).execute()

    # Trigger background indexing
    indexing_service = IndexingService(github_service)
    background_tasks.add_task(
        indexing_service.index_repository,
        repository_id=repo_id,
        github_url=payload.github_url,
        branch=payload.branch or "main"
    )

    return repo_data


@router.get("/{id}", response_model=RepositoryResponse)
async def get_repository(id: str):
    """Get repository details."""
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=404, detail="Repository not found")

    res = supabase.table("repositories").select("*").eq("id", id).maybe_single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Repository not found")
    return res.data


@router.delete("/{id}")
async def disconnect_repository(id: str):
    """Disconnect a repository and delete associated code chunks."""
    supabase = get_supabase_client()
    if supabase:
        supabase.table("code_chunks").delete().eq("repository_id", id).execute()
        supabase.table("repositories").delete().eq("id", id).execute()
    return {"message": "Repository removed successfully"}


@router.post("/{id}/index")
async def trigger_indexing(id: str, background_tasks: BackgroundTasks):
    """Manually trigger or re-index a repository."""
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=404, detail="Repository not found")

    res = supabase.table("repositories").select("*").eq("id", id).maybe_single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Repository not found")

    repo = res.data
    indexing_service = IndexingService()
    background_tasks.add_task(
        indexing_service.index_repository,
        repository_id=repo["id"],
        github_url=repo["github_url"],
        branch=repo.get("branch", "main")
    )
    return {"message": "Indexing started", "repository_id": id}
