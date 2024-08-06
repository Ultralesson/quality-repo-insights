from pydantic import BaseModel


class RepoInfo(BaseModel):
    name: str = None
    git_initialized: bool = False
    type: str = None
    head_commit_sha: str = None
    branch: str = None
    repo_path: str = None
