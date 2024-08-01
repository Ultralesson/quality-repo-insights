import os

from langchain import requests


class RepoDetailsUserInteractions:
    @staticmethod
    def get_repo_type():
        repo_type = ''
        while repo_type == '':
            repo_type = input("Repository Type:\n1. GitHub\n2. Local\nSelect 1 or 2: ")
            if repo_type.strip() == '1' or repo_type.strip() == '2':
                return repo_type

    @staticmethod
    def get_repo_path(repo_type):
        def is_repo_type_github():
            return repo_type == '1'

        valid_repo_path = False

        while not valid_repo_path:
            repo_path = input(f'\n\nEnter the repo {'url' if is_repo_type_github() else 'path'}: ')

            if is_repo_type_github():
                valid_repo_path = requests.get(repo_path).status_code == 200
            else:
                valid_repo_path = os.path.exists(repo_path)

            if valid_repo_path:
                repo_name = repo_path.split('/')[-1]
                return repo_name, repo_path
