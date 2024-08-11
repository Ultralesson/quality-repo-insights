import os
from abc import abstractmethod
from typing import Dict, List

from chunker import chunker_mapper
from chunker.chunker import Chunker


class Traverser:

    @abstractmethod
    def extract_contents(self) -> Dict[str, List[str]]:
        pass

    @staticmethod
    def _chunk_content(file_name: str, text: str) -> Dict:
        _, file_extension = os.path.splitext(file_name)
        file_type = file_extension.lower()
        if file_type in chunker_mapper:
            chunker: Chunker = chunker_mapper[file_type]()
            file_elements = chunker.chunk_file(text)
            return file_elements

        return {}
