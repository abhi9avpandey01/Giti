import base64
import os
import httpx
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from app.config import settings

# File exclusions based on PRD Section 10.1
EXCLUDED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".mp4", ".mp3", ".wav", ".avi", ".mov",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".pdf", ".exe", ".bin", ".dll", ".so", ".dylib",
    ".pyc", ".pyo", ".pyd", ".class",
    ".lock", ".map"
}

EXCLUDED_DIRECTORIES = {
    "node_modules", ".git", ".next", "dist", "build", "out",
    "venv", ".venv", "env", "__pycache__", ".idea", ".vscode",
    "coverage", ".pytest_cache"
}

SUPPORTED_CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java",
    ".c", ".cpp", ".h", ".hpp", ".cs", ".rb", ".php", ".swift",
    ".kt", ".scala", ".sql", ".sh", ".yaml", ".yml", ".json", ".md"
}


class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    @staticmethod
    def parse_repo_url(url: str) -> tuple[str, str]:
        """Parses owner and repo name from GitHub URL."""
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.strip("/").split("/") if p]
        if len(path_parts) < 2:
            raise ValueError(f"Invalid GitHub repository URL: {url}")
        owner, repo = path_parts[0], path_parts[1].replace(".git", "")
        return owner, repo

    async def get_repository_metadata(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetches repository metadata from GitHub REST API."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=self.headers,
                timeout=15.0
            )
            resp.raise_for_status()
            return resp.json()

    async def get_latest_commit_sha(self, owner: str, repo: str, branch: str = "main") -> str:
        """Retrieves head commit SHA for specified branch."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}",
                headers=self.headers,
                timeout=15.0
            )
            resp.raise_for_status()
            return resp.json()["sha"]

    async def fetch_repository_tree(self, owner: str, repo: str, commit_sha: str) -> List[Dict[str, Any]]:
        """Retrieves git tree recursively for repository files."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/git/trees/{commit_sha}?recursive=1",
                headers=self.headers,
                timeout=30.0
            )
            resp.raise_for_status()
            data = resp.json()
            tree = data.get("tree", [])

            # Filter valid code files
            valid_files = []
            for item in tree:
                if item.get("type") != "blob":
                    continue
                path = item.get("path", "")
                parts = path.split("/")
                # Check excluded directory
                if any(p in EXCLUDED_DIRECTORIES for p in parts):
                    continue
                _, ext = os.path.splitext(path)
                if ext.lower() in EXCLUDED_EXTENSIONS:
                    continue
                if ext.lower() in SUPPORTED_CODE_EXTENSIONS or os.path.basename(path).lower() in ["dockerfile", "makefile", "gemfile"]:
                    valid_files.append(item)
            return valid_files

    async def fetch_file_content(self, owner: str, repo: str, file_sha: str) -> str:
        """Fetches and decodes file content by git blob SHA."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{file_sha}",
                headers=self.headers,
                timeout=15.0
            )
            resp.raise_for_status()
            blob_data = resp.json()
            raw_content = blob_data.get("content", "")
            encoding = blob_data.get("encoding", "")
            if encoding == "base64":
                return base64.b64decode(raw_content).decode("utf-8", errors="ignore")
            return raw_content
