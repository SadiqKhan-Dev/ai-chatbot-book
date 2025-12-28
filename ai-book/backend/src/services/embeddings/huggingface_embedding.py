"""
Hugging Face embedding service.
Uses sentence-transformers for local embedding generation.
"""

from typing import Optional

from sentence_transformers import SentenceTransformer

from .base import BaseEmbeddingService


class HuggingFaceEmbeddingService(BaseEmbeddingService):
    """Embedding service using Hugging Face sentence-transformers."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
    ):
        """Initialize Hugging Face embedding service."""
        super().__init__(model_name, None)

        # Initialize sentence-transformers model
        self._model = SentenceTransformer(model_name, device=device)

        # Get dimension from model
        self._dimension = self._model.get_sentence_embedding_dimension()

    @property
    def dimension(self) -> int:
        """Return embedding dimension for the model."""
        return self._dimension

    def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text using HF."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        embedding = self._model.encode(text.strip(), normalize_embeddings=True)
        return embedding.tolist()

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple documents."""
        if not documents:
            return []

        # Filter out empty documents
        valid_docs = [doc.strip() for doc in documents if doc.strip()]

        if not valid_docs:
            return [[0.0] * self.dimension for _ in documents]

        # Batch encode with normalization
        embeddings = self._model.encode(
            valid_docs,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        # Convert to list of lists
        embedding_list = embeddings.tolist()

        # Handle case where some documents were empty
        result: list[list[float]] = []
        doc_idx = 0
        for doc in documents:
            if doc.strip():
                result.append(embedding_list[doc_idx])
                doc_idx += 1
            else:
                result.append([0.0] * self.dimension)

        return result

    async def aembed(self, text: str) -> list[float]:
        """Async embedding - uses sync method for HF."""
        return self.embed(text)

    async def aembed_batch(self, texts: list[str]) -> list[list[float]]:
        """Async batch embedding - uses sync method for HF."""
        return self.embed_documents(texts)
