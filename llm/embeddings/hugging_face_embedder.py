from sentence_transformers import SentenceTransformer
from llm.embeddings import EmbeddingContract
from transformers import AutoTokenizer
import numpy as np


class HuggingFaceEmbedder(EmbeddingContract):

    def __init__(self, model="sentence-transformers/all-MiniLM-L6-v2"):
        self._embedding_model = SentenceTransformer(model)
        self._tokenizer = AutoTokenizer.from_pretrained(model)

    def generate_embeddings(self, text):
        """
        Generates embeddings for the given text using Sentence Transformer.
        """
        embedding = self._embedding_model.encode(text)
        embedding = np.array(embedding)

        if embedding.ndim != 1:
            raise ValueError(
                f"Expected 1D array for embedding, but got shape: {format(embedding.shape)}"
            )

        return embedding

    def split_text_into_chunks(self, text, max_tokens=510):
        """
        Splits the text into chunks of approximate size based on max_tokens.
        """
        tokens = self._tokenizer.encode(text, add_special_tokens=False)
        chunks = [tokens[i : i + max_tokens] for i in range(0, len(tokens), max_tokens)]
        return [self._tokenizer.decode(chunk) for chunk in chunks]
