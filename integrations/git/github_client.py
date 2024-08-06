import re

from config import GITHUB_ACCESS_TOKEN
from github import Github, Auth, GithubException


class GitHubClient:
    def __init__(self, repo_path):
        self.__client = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
        self.__full_name = self.__extract_repo_details(repo_path)

    @property
    def __repo(self):
        return self.__client.get_repo(self.__full_name)

    def get_changed_files(self, start_commit, end_commit="HEAD"):
        comparison = self.__repo.compare(start_commit, end_commit)
        return [file.filename for file in comparison.files]

    def get_default_branch(self):
        return self.__repo.default_branch

    def get_head_commit(self, branch: str = None):
        branch_obj = (
            self.__repo.get_branch(self.__repo.default_branch)
            if branch is None
            else self.__repo.get_branch(branch)
        )

        return branch_obj.commit.sha

    def get_contents(self, path: str, branch: str = None):
        if branch is None:
            return self.__repo.get_contents(path)
        else:
            return self.__repo.get_contents(path, ref=branch)

    def branch_exists(self, branch: str):
        try:
            self.__repo.get_branch(branch)
            return True
        except GithubException as e:
            if e.status == 404:
                print(f"Branch {branch} doesn't exist")
            return False

    @staticmethod
    def __extract_repo_details(repo_path: str):
        pattern = r"https://github.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)"
        match = re.match(pattern, repo_path)
        if match:
            return f"{match.group('owner')}/{match.group('repo')}"
        else:
            raise ValueError(f"Invalid GitHub URL: {repo_path}")
