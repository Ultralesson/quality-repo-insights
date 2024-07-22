from transformers import AutoTokenizer, AutoModel
from llm.contracts import EmbeddingContract
import torch


class CodeBertEmbeddings(EmbeddingContract):
    def __init__(self, model='microsoft/codebert-base'):
        self._tokenizer = AutoTokenizer.from_pretrained(model)
        self._model = AutoModel.from_pretrained(model)

    def generate_embeddings(self, text):
        inputs = self._tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self._model(**inputs)

        return outputs.last_hidden_state[:, 0, :].numpy().flatten()

    def split_text_into_chunks(self, text, max_tokens=512):
        tokens = self._tokenizer.encode(text, add_special_tokens=False)
        chunks = [tokens[i: i + max_tokens] for i in range(0, len(tokens), max_tokens)]
        return [self._tokenizer.decode(chunk) for chunk in chunks]
