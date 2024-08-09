import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from chunker import JavaFileChunker
from repo_traverser.ignore_patterns.ignore_patterns import IGNORE_PATTERNS
from repo_traverser.traverser import Traverser


class LocalRepoTraverser(Traverser):
    def __init__(self, repo_path: str):
        super().__init__()
        self._repo_path = repo_path if repo_path.endswith("/") else f"{repo_path}/"

    async def extract_contents(self, max_tokens=512) -> Dict[str, List[str]]:
        loop = asyncio.get_event_loop()
        file_info = {}
        futures = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for dir_path, dir_names, file_names in os.walk(self._repo_path):
                if dir_path == self._repo_path:
                    continue

                if self.__should_ignore(dir_path):
                    dir_names[:] = []
                    continue

                dir_names[:] = [
                    dir_name
                    for dir_name in dir_names
                    if not self.__should_ignore(os.path.join(dir_path, dir_name))
                ]

                file_names[:] = [
                    file_name
                    for file_name in file_names
                    if not self.__should_ignore(os.path.join(dir_path, file_name))
                ]

                for file_name in file_names:
                    future = loop.run_in_executor(
                        executor, self.__process_file, dir_path, file_name
                    )
                    futures.append(future)

            results = await asyncio.gather(*futures)

            for result in results:
                file_name, chunks = result
                file_info[file_name] = chunks

        return file_info

    def __process_file(self, dir_path: str, file_name: str):
        file = os.path.join(dir_path, file_name)
        rel_file_name = os.path.normpath(file.split(self._repo_path)[-1])
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                chunks = JavaFileChunker().chunk_file(content) if file_name.endswith(".java") else []
                return rel_file_name, chunks
        except Exception as e:
            print(f"Could not read file {file}: {e}")
            return rel_file_name, None

    def __should_ignore(self, path):
        normalized_path = os.path.normpath(path)
        basename = os.path.basename(normalized_path)
        repo = (
            self._repo_path + "/"
            if not self._repo_path.endswith("/")
            else self._repo_path
        )

        if basename in IGNORE_PATTERNS or normalized_path in IGNORE_PATTERNS:
            return True

        for part in normalized_path.split(repo):
            if part in IGNORE_PATTERNS:
                return True

        return False
