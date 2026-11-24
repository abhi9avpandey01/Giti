from fastapi import APIRouter
from app.services.indexing_service import IndexingService

router = APIRouter(prefix="/api/indexing", tags=["Indexing"])


@router.get("/status/{repository_id}")
async def get_indexing_status(repository_id: str):
    """Check indexing status of repository."""
    from app.database.redis import cache_get
    status = await cache_get(f"indexing_status:{repository_id}")
    return {"repository_id": repository_id, "status": status or "unknown"}
