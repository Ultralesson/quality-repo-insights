from llm.contracts import EmbeddingContract
from openai import OpenAI

client = OpenAI()


class OpenAIEmbedding(EmbeddingContract):
    def __init__(self, model):
        self._model = model

    def generate_embeddings(self, text):
        """
        Generates embeddings for the given text using OpenAI's API.
        """
        response = client.embeddings.create(
            input=text,
            model=self._model
        )

        return response.data[0].embedding

    def split_text_into_chunks(self, text, max_tokens=2048):
        """
        Splits the text into chunks of approximate size based on max_tokens.
        """
        sentences = text.split('.')
        chunks = []
        current_chunk = ''

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_tokens:
                current_chunk += sentence + '.'
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + '.'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
