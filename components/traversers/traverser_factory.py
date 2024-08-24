from components.traversers import GitHubTraverser, LocalRepoTraverser
from components.traversers.traverser import Traverser


class TraverserFactory:
    @staticmethod
    def create_traverser(repo_type: str, repo_path: str) -> Traverser:
        if repo_type.lower() == "github":
            return GitHubTraverser(repo_path)
        elif repo_type.lower() == "local":
            return LocalRepoTraverser(repo_path)
        else:
            raise ValueError(f"Unsupported repository type: {repo_type}")
