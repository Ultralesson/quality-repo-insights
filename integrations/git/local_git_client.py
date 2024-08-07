from typing import List
from warnings import warn

from git import Repo, InvalidGitRepositoryError


class LocalGitClient:
    def __init__(self, repo_path):
        self.__repo_path = repo_path

    def get_changed_files(self, start_commit, end_commit="HEAD") -> List[str]:
        if self.__repo is None:
            return []

        diff = self.__repo.git.diff("--name-only", start_commit, end_commit)
        return diff.split("\n")

    def get_default_branch(self) -> str:
        return self.__repo.active_branch.name

    def get_head_commit(self) -> str:
        return self.__repo.head.commit.hexsha

    def git_initialized(self):
        return self.__repo is not None

    @property
    def __repo(self):
        try:
            repo = Repo(self.__repo_path)
            if repo.bare:
                return None
            return repo
        except InvalidGitRepositoryError as e:
            warn(str(e))
            return None
