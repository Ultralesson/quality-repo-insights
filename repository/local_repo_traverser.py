import os
from llm.contracts import EmbeddingContract
from repository.ignore_patterns.ignore_patterns import IGNORE_PATTERNS


class LocalRepoTraverser:
    def __init__(self, repo_path: str, embedder: EmbeddingContract):
        self._repo_path = repo_path
        self._embedder = embedder

    def extract_folder_structure_and_contents(self, max_tokens=512):
        ignore_patterns = IGNORE_PATTERNS
        folder_structure = {}

        def should_ignore(path):
            normalized_path = os.path.normpath(path)
            basename = os.path.basename(normalized_path)
            repo = self._repo_path + '/' if not self._repo_path.endswith('/') else self._repo_path

            if basename in ignore_patterns or normalized_path in ignore_patterns:
                return True

            for part in normalized_path.split(repo):
                if part in ignore_patterns:
                    return True

            return False

        for dirpath, dirnames, filenames in os.walk(self._repo_path):
            if dirpath == self._repo_path:
                continue

            if should_ignore(dirpath):
                dirnames[:] = []
                continue

            dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d))]
            filenames[:] = [f for f in filenames if not should_ignore(os.path.join(dirpath, f))]

            folder = os.path.relpath(dirpath, self._repo_path)

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        chunks = self._embedder.split_text_into_chunks(content, max_tokens)
                        embeddings = [self._embedder.generate_embeddings(chunk) for chunk in chunks]

                        folder_structure[folder] = []
                        folder_structure[folder].append({
                            'file_name': filename,
                            'content': content,
                            'chunks': chunks,
                            'embeddings': embeddings
                        })
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

        return folder_structure
