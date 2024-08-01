import os

from repo_traverser.ignore_patterns.ignore_patterns import IGNORE_PATTERNS
from repo_traverser.traverser import Traverser


class LocalRepoTraverser(Traverser):
    def __init__(self, repo_path: str, embedder):
        self._repo_path = repo_path if repo_path.endswith('/') else f"{repo_path}/"
        self._embedder = embedder

    def extract_folder_structure_and_contents(self, max_tokens=512):
        folder_structure = {}

        for dirpath, dirnames, filenames in os.walk(self._repo_path):
            if dirpath == self._repo_path:
                continue

            if self.__should_ignore(dirpath):
                dirnames[:] = []
                continue

            dirnames[:] = [d for d in dirnames if not self.__should_ignore(os.path.join(dirpath, d))]
            filenames[:] = [f for f in filenames if not self.__should_ignore(os.path.join(dirpath, f))]

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                rel_file_name = os.path.normpath(file_path.split(self._repo_path)[-1])

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        chunks = self._embedder.split_text_into_chunks(content, max_tokens)
                        embeddings = [self._embedder.generate_embeddings(chunk) for chunk in chunks]

                        folder_structure[rel_file_name] = {
                            'content': content,
                            'chunks': chunks,
                            'embeddings': embeddings
                        }
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

        return folder_structure

    def __should_ignore(self, path):
        normalized_path = os.path.normpath(path)
        basename = os.path.basename(normalized_path)
        repo = self._repo_path + '/' if not self._repo_path.endswith('/') else self._repo_path

        if basename in IGNORE_PATTERNS or normalized_path in IGNORE_PATTERNS:
            return True

        for part in normalized_path.split(repo):
            if part in IGNORE_PATTERNS:
                return True

        return False
