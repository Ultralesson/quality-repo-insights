import fnmatch
import re
from collections import deque

from github import Github, Auth

from config import GITHUB_ACCESS_TOKEN
from llm.embeddings import EmbeddingContract
from repo_traverser.ignore_patterns.ignore_patterns import IGNORE_PATTERNS
from repo_traverser.traverser import Traverser


class GitHubTraverser(Traverser):
    def __init__(self, repo_path: str, embedder: EmbeddingContract):
        self.__repo_path = repo_path
        self.__client = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
        self.__embedder = embedder

    def extract_folder_structure_and_contents(self):
        folder_structure = {}
        queue = deque([""])

        owner, repo_name = self.__extract_repo_details()
        repo = self.__client.get_repo(f"{owner}/{repo_name}")

        while queue:
            current_folder = queue.popleft()
            contents = repo.get_contents(current_folder)

            for content in contents:
                if self.__should_ignore(content.path):
                    continue

                if content.type == "dir":
                    queue.append(content.path)
                else:
                    file_content = repo.get_contents(
                        content.path
                    ).decoded_content.decode("utf-8")
                    chunks = self.__embedder.split_text_into_chunks(file_content)
                    embeddings = [
                        self.__embedder.generate_embeddings(chunk) for chunk in chunks
                    ]
                    folder_structure[content.path] = {
                        "content": file_content,
                        "chunks": chunks,
                        "embeddings": embeddings,
                    }

        return folder_structure

    def __extract_repo_details(self):
        pattern = r"https://github.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)"
        match = re.match(pattern, self.__repo_path)
        if match:
            return match.group("owner"), match.group("repo")
        else:
            raise ValueError(f"Invalid GitHub URL: {self.__repo_path}")

    @staticmethod
    def __should_ignore(path: str):
        if any(
            fnmatch.fnmatch(path.split("/")[-1], pattern) for pattern in IGNORE_PATTERNS
        ):
            return True

        for pattern in IGNORE_PATTERNS:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, pattern):
                return True

        return False
