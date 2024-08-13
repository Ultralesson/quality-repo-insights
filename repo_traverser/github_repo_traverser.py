import asyncio
import fnmatch
import re
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from github import Github, Auth

from config import GITHUB_ACCESS_TOKEN
from repo_traverser.ignore_patterns.ignore_patterns import IGNORE_PATTERNS
from repo_traverser.traverser import Traverser


class GitHubTraverser(Traverser):
    def __init__(self, repo_path: str):
        super().__init__()
        self.__repo_path = repo_path
        self.__client = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
        self.__embedder_lock = threading.Lock()

    async def extract_contents(self) -> Dict[str, str]:
        file_info = {}
        queue = deque([""])

        owner, repo_name = self.__extract_repo_details()
        repo = self.__client.get_repo(f"{owner}/{repo_name}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            while queue:
                current_folder = queue.popleft()
                contents = repo.get_contents(current_folder)

                for content in contents:
                    if self.__should_ignore(content.path):
                        continue

                    if content.type == "dir":
                        queue.append(content.path)
                    else:
                        future = loop.run_in_executor(
                            executor, self.__process_file, content.path, repo
                        )
                        futures.append(future)

            results = await asyncio.gather(*futures)

            for result in results:
                file_name, content = result
                file_info[file_name] = content

        return file_info

    @staticmethod
    def __process_file(file_path, repo):
        file_content = repo.get_contents(file_path).decoded_content.decode()
        return file_path, file_content

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
