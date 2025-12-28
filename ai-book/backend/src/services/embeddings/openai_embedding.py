"""
OpenAI embedding service.
Uses OpenAI's text-embedding-3-small model.
"""

from typing import Optional

from langchain_openai import OpenAIEmbeddings as LangChainOpenAIEmbeddings

from .base import BaseEmbeddingService


class OpenAIEmbeddingService(BaseEmbeddingService):
    """Embedding service using OpenAI's embedding models."""

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
    ):
        super().__init__(model_name, api_key)

        # Initialize LangChain embedding model
        self._embedding_model = LangChainOpenAIEmbeddings(
            model=self.model_name,
            api_key=api_key,
        )

    @property
    def dimension(self) -> int:
        """Return embedding dimension for text-embedding-3-small."""
        # text-embedding-3-small produces 1536 dimensions
        return 1536

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text using OpenAI."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        # Use LangChain's embed_query for single texts
        embedding = self._embedding_model.embed_query(text.strip())
        return embedding

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple documents."""
        if not documents:
            return []

        # Filter out empty documents
        valid_docs = [doc.strip() for doc in documents if doc.strip()]

        if not valid_docs:
            return [[0.0] * self.dimension for _ in documents]

        # Use LangChain's embed_documents for batch
        embeddings = self._embedding_model.embed_documents(valid_docs)

        # Handle case where some documents were empty
        result: list[list[float]] = []
        doc_idx = 0
        for doc in documents:
            if doc.strip():
                result.append(embeddings[doc_idx])
                doc_idx += 1
            else:
                result.append([0.0] * self.dimension)

        return result

    async def aembed(self, text: str) -> list[float]:
        """Async embedding - uses sync method for OpenAI."""
        return self.embed(text)

    async def aembed_batch(self, texts: list[str]) -> list[list[float]]:
        """Async batch embedding - uses sync method for OpenAI."""
        return self.embed_batch(texts, show_progress=False)
