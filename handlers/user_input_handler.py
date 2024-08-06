import os

import requests

from integrations.git import GitHubClient
from integrations.git.local_git_client import LocalGitClient
from handlers.models.repo_info import RepoInfo


class UserRepoInfoHandler:

    def get_repo_info(self) -> RepoInfo:
        repo_type = self.__get_repo_type()
        is_repo_path_valid = False
        repo_path = ""

        def is_repo_type_github():
            return repo_type == "1"

        while not is_repo_path_valid:
            repo_path = input(
                f"\n\nEnter the repo {'url' if is_repo_type_github() else 'path'}: "
            )

            if is_repo_type_github():
                is_repo_path_valid = requests.get(repo_path).status_code == 200

            else:
                is_repo_path_valid = os.path.exists(repo_path)

        branch, head_commit_sha = (
            self.__get_github_branch_and_commit_details(repo_path)
            if is_repo_type_github()
            else self.__get_local_branch_and_commit_details(repo_path)
        )

        return RepoInfo(
            name=repo_path.split("/")[-1],
            git_initialized=head_commit_sha.split() != "" and branch != "",
            type="GitHub" if is_repo_type_github() else "Local",
            head_commit_sha=head_commit_sha,
            branch=branch,
            repo_path=repo_path,
        )

    @staticmethod
    def __get_github_branch_and_commit_details(repo_path):
        github_client = GitHubClient(repo_path)
        default_branch = github_client.get_default_branch()

        branch_input = input(
            f"""Branch {default_branch} will be reviewed. 
            Press Enter to continue or specify the branch name to be reviewed:
            """
        )

        def check_branch(user_input):
            branch_name = default_branch if branch_input.strip() == "" else user_input
            return branch_name, github_client.branch_exists(branch_name)

        branch, branch_exists = check_branch(branch_input)

        while not branch_exists:
            branch_input = input(
                f"""Branch {branch} doesn't exist. Do you want to get the review for {default_branch}?
                Press Enter to proceed or specify the correct branch name: 
                """
            )

            branch, branch_exists = check_branch(branch_input)

        head_commit_sha = github_client.get_head_commit()
        return branch, head_commit_sha

    @staticmethod
    def __get_local_branch_and_commit_details(repo_path):
        git_client = LocalGitClient(repo_path)

        if not git_client.git_initialized():
            return None, None

        default_branch = git_client.get_default_branch()
        head_commit_sha = git_client.get_head_commit()
        return default_branch, head_commit_sha

    @staticmethod
    def __get_repo_type():
        repo_type = ""
        while repo_type == "":
            repo_type = input("Repository Type:\n1. GitHub\n2. Local\nSelect 1 or 2: ")
            if repo_type.strip() == "1" or repo_type.strip() == "2":
                break

        return repo_type
