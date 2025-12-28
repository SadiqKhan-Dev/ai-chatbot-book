"""
Cohere embedding service.
Uses Cohere's embedding models for text vectorization.
"""

from typing import Optional

import cohere
from cohere import Client as CohereClient

from .base import BaseEmbeddingService


class CohereEmbeddingService(BaseEmbeddingService):
    """Embedding service using Cohere's embedding models."""

    def __init__(
        self,
        model_name: str = "embed-english-v3.0",
        api_key: Optional[str] = None,
    ):
        """Initialize Cohere embedding service."""
        super().__init__(model_name, api_key)

        # Initialize Cohere client
        self._client = CohereClient(api_key=api_key)

        # Set dimension based on model
        self._dimension = self._get_dimension_for_model(model_name)

    def _get_dimension_for_model(self, model_name: str) -> int:
        """Get embedding dimension for Cohere model."""
        # v3 models use 1024 dimensions
        if "v3" in model_name:
            return 1024
        # v2 models use 4096 dimensions
        elif "v2" in model_name:
            return 4096
        # Default to 1024
        return 1024

    @property
    def dimension(self) -> int:
        """Return embedding dimension for the model."""
        return self._dimension

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text using Cohere."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        response = self._client.embed(
            texts=[text.strip()],
            model=self.model_name,
            input_type="search_query",
        )

        return response.embeddings[0]

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple documents."""
        if not documents:
            return []

        # Filter out empty documents
        valid_docs = [doc.strip() for doc in documents if doc.strip()]

        if not valid_docs:
            return [[0.0] * self.dimension for _ in documents]

        # Batch embed with Cohere (max batch size is 96)
        batch_size = 96
        all_embeddings: list[list[float]] = []

        for i in range(0, len(valid_docs), batch_size):
            batch = valid_docs[i : i + batch_size]
            response = self._client.embed(
                texts=batch,
                model=self.model_name,
                input_type="search_document",
            )
            all_embeddings.extend(response.embeddings)

        # Handle case where some documents were empty
        result: list[list[float]] = []
        doc_idx = 0
        for doc in documents:
            if doc.strip():
                result.append(all_embeddings[doc_idx])
                doc_idx += 1
            else:
                result.append([0.0] * self.dimension)

        return result

    async def aembed(self, text: str) -> list[float]:
        """Async embedding - uses sync method for Cohere."""
        return self.embed(text)

    async def aembed_batch(self, texts: list[str]) -> list[list[float]]:
        """Async batch embedding - uses sync method for Cohere."""
        return self.embed_documents(texts)
