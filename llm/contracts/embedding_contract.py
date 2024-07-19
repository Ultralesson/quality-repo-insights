from abc import abstractmethod


class EmbeddingContract:
    @abstractmethod
    def generate_embeddings(self, text):
        pass

    @abstractmethod
    def split_text_into_chunks(self, text, max_tokens=512):
        pass
