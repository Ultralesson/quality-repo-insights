import os

from langchain import requests

from database.supabase import SupabaseDataClient
from database.supabase.clients import RepositoryTableClient
from database.supabase.models import Repository
from repo_traverser import GitHubTraverser, LocalRepoTraverser


class RepoDetailsUserInteractions:

    def get_repo_details(self):
        repo_type = self.__get_repo_type()
        valid_repo_path = False

        def is_repo_type_github():
            return repo_type == "1"

        def traverser(repo):
            return (
                GitHubTraverser(repo)
                if is_repo_type_github()
                else LocalRepoTraverser(repo)
            )

        while not valid_repo_path:
            repo_path = input(
                f"\n\nEnter the repo {'url' if is_repo_type_github() else 'path'}: "
            )

            if is_repo_type_github():
                valid_repo_path = requests.get(repo_path).status_code == 200
            else:
                valid_repo_path = os.path.exists(repo_path)

            if valid_repo_path:
                repo_name = repo_path.split("/")[-1]
                repo_id = RepositoryTableClient().add_repository(
                    Repository(name=repo_name, url=repo_path)
                )

                return repo_id, traverser(repo_path)

    @staticmethod
    def __get_repo_type():
        repo_type = ""
        while repo_type == "":
            repo_type = input("Repository Type:\n1. GitHub\n2. Local\nSelect 1 or 2: ")
            if repo_type.strip() == "1" or repo_type.strip() == "2":
                return repo_type
