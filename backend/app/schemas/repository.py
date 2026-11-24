from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class RepositoryConnectRequest(BaseModel):
    github_url: str = Field(..., description="Full GitHub repository URL e.g. https://github.com/owner/repo")
    branch: Optional[str] = Field("main", description="Target branch to index")


class RepositoryResponse(BaseModel):
    id: str
    user_id: str
    github_url: str
    name: str
    branch: str
    commit_sha: Optional[str] = None
    indexing_status: str  # pending, indexing, completed, failed
    created_at: Optional[datetime] = None


class CodeChunk(BaseModel):
    id: Optional[str] = None
    repository_id: str
    file_path: str
    start_line: int
    end_line: int
    content: str
    embedding: Optional[List[float]] = None
