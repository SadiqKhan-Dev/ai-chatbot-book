"""
Base embedding service interface.
Defines the contract for all embedding providers.
"""

from abc import ABC, abstractmethod
from typing import List

from tqdm import tqdm


class BaseEmbeddingService(ABC):
    """Abstract base class for embedding services."""

    def __init__(self, model_name: str, api_key: str | None = None):
        self.model_name = model_name
        self.api_key = api_key

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the embedding dimension for this model."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        pass

    def embed_batch(
        self, texts: List[str], show_progress: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of texts to embed
            show_progress: Whether to show progress bar

        Returns:
            List of embedding vectors
        """
        embeddings: List[List[float]] = []

        iterator = tqdm(
            texts,
            desc="Generating embeddings",
            disable=not show_progress,
        )

        for text in iterator:
            embedding = self.embed(text)
            embeddings.append(embedding)

        return embeddings

    def embed_with_retry(
        self, text: str, max_retries: int = 3
    ) -> list[float]:
        """Generate embedding with automatic retry on failure."""
        import time

        for attempt in range(max_retries):
            try:
                return self.embed(text)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    time.sleep(wait_time)
                else:
                    raise e

    def batch_embed_with_retry(
        self, texts: List[str], max_retries: int = 3
    ) -> List[List[float]]:
        """Generate embeddings for batch with retry on failure."""
        import time

        successful_embeddings: List[List[float]] = []
        failed_indices: List[int] = []

        for i, text in enumerate(texts):
            for attempt in range(max_retries):
                try:
                    embedding = self.embed(text)
                    successful_embeddings.append(embedding)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2
                        time.sleep(wait_time)
                    elif i == len(texts) - 1:
                        raise e
                    else:
                        failed_indices.append(i)

        # Retry failed texts
        for i in failed_indices:
            for attempt in range(max_retries):
                try:
                    embedding = self.embed(texts[i])
                    successful_embeddings.append(embedding)
                    break
                except Exception:
                    if attempt == max_retries - 1:
                        # Use zero vector as fallback
                        successful_embeddings.append([0.0] * self.dimension)

        return successful_embeddings
