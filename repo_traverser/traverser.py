from abc import abstractmethod
from typing import Dict, List

from transformers import AutoTokenizer, AutoModel


class Traverser:
    def __init__(self, model="microsoft/codebert-base"):
        self._tokenizer = AutoTokenizer.from_pretrained(model)
        self._model = AutoModel.from_pretrained(model)

    @abstractmethod
    def extract_contents(self) -> Dict[str, List[str]]:
        pass

    def _split_text_into_chunks(self, text, max_tokens=512):
        tokens = self._tokenizer.encode(text, add_special_tokens=False)
        chunks = [tokens[i: i + max_tokens] for i in range(0, len(tokens), max_tokens)]
        return [self._tokenizer.decode(chunk) for chunk in chunks]
