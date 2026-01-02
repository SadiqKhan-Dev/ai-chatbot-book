"""
Base embedding service interface.
Defines the contract for all embedding providers.
"""

import hashlib
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, List, Optional

from tqdm import tqdm

logger = logging.getLogger(__name__)


class EmbeddingCache:
    """Simple file-based cache for embeddings to avoid redundant API calls."""

    def __init__(self, cache_dir: Optional[str] = None, max_size_mb: int = 100):
        """
        Initialize the embedding cache.

        Args:
            cache_dir: Directory to store cache files (default: ~/.cache/ai-book-embeddings)
            max_size_mb: Maximum cache size in megabytes
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "ai-book-embeddings"
        else:
            cache_dir = Path(cache_dir)

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self._index_file = self.cache_dir / "cache_index.json"

        # Load existing index
        self._index: dict[str, dict] = self._load_index()

    def _load_index(self) -> dict:
        """Load the cache index from disk."""
        if self._index_file.exists():
            try:
                with open(self._index_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load cache index: {e}")
                return {}
        return {}

    def _save_index(self):
        """Save the cache index to disk."""
        with open(self._index_file, "w") as f:
            json.dump(self._index, f)

    def _get_content_hash(self, text: str) -> str:
        """Generate a hash for the content."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _get_cache_path(self, content_hash: str) -> Path:
        """Get the path for a cached embedding."""
        return self.cache_dir / f"{content_hash}.json"

    def get(self, text: str) -> Optional[List[float]]:
        """
        Get a cached embedding for the given text.

        Args:
            text: The text to look up

        Returns:
            The cached embedding or None if not found
        """
        content_hash = self._get_content_hash(text)
        cache_path = self._get_cache_path(content_hash)

        if cache_path.exists() and content_hash in self._index:
            try:
                with open(cache_path, "r") as f:
                    data = json.load(f)
                    return data["embedding"]
            except (json.JSONDecodeError, IOError, KeyError) as e:
                logger.warning(f"Failed to read cached embedding: {e}")
                # Clean up corrupted entry
                cache_path.unlink(missing_ok=True)
                self._index.pop(content_hash, None)
                self._save_index()

        return None

    def set(self, text: str, embedding: List[float]):
        """
        Cache an embedding for the given text.

        Args:
            text: The text that was embedded
            embedding: The resulting embedding vector
        """
        content_hash = self._get_content_hash(text)
        cache_path = self._get_cache_path(content_hash)

        # Check cache size and clean up if necessary
        self._cleanup_if_needed()

        try:
            with open(cache_path, "w") as f:
                json.dump(
                    {
                        "text": text,
                        "embedding": embedding,
                        "created_at": str(Path(cache_path).stat().st_mtime),
                    },
                    f,
                )
            self._index[content_hash] = {
                "path": str(cache_path),
                "size": len(json.dumps(embedding)),
            }
            self._save_index()
        except IOError as e:
            logger.warning(f"Failed to cache embedding: {e}")

    def _cleanup_if_needed(self):
        """Clean up old cache entries if size limit is reached."""
        total_size = sum(entry.get("size", 0) for entry in self._index.values())

        if total_size < self.max_size_bytes:
            return

        # Sort by creation time and remove oldest entries
        entries = []
        for content_hash, entry in self._index.items():
            cache_path = Path(entry["path"])
            if cache_path.exists():
                mtime = cache_path.stat().st_mtime
                entries.append((mtime, content_hash, entry))

        entries.sort(key=lambda x: x[0])

        # Remove oldest 20% of entries
        to_remove = int(len(entries) * 0.2)
        for _, content_hash, entry in entries[:to_remove]:
            cache_path = Path(entry["path"])
            cache_path.unlink(missing_ok=True)
            self._index.pop(content_hash, None)

        self._save_index()

    def clear(self):
        """Clear all cached embeddings."""
        for content_hash, entry in self._index.items():
            cache_path = Path(entry["path"])
            cache_path.unlink(missing_ok=True)
        self._index = {}
        self._save_index()
        logger.info("Embedding cache cleared")

    @property
    def size_bytes(self) -> int:
        """Get the current cache size in bytes."""
        return sum(entry.get("size", 0) for entry in self._index.values())

    @property
    def entry_count(self) -> int:
        """Get the number of cached entries."""
        return len(self._index)


class BaseEmbeddingService(ABC):
    """Abstract base class for embedding services."""

    def __init__(
        self,
        model_name: str,
        api_key: str | None = None,
        cache_dir: str | None = None,
        cache_enabled: bool = True,
    ):
        """
        Initialize the embedding service.

        Args:
            model_name: Name of the embedding model
            api_key: Optional API key
            cache_dir: Directory for embedding cache
            cache_enabled: Whether to enable embedding cache
        """
        self.model_name = model_name
        self.api_key = api_key
        self._cache: Optional[EmbeddingCache] = None
        self._cache_enabled = cache_enabled
        self._cache_dir = cache_dir

    def _get_cache(self) -> EmbeddingCache:
        """Get or create the embedding cache."""
        if self._cache is None:
            self._cache = EmbeddingCache(cache_dir=self._cache_dir)
        return self._cache

    @property
    def cache(self) -> Optional[EmbeddingCache]:
        """Get the embedding cache if enabled."""
        return self._get_cache() if self._cache_enabled else None

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
        self,
        texts: List[str],
        show_progress: bool = True,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of texts to embed
            show_progress: Whether to show progress bar
            progress_callback: Optional callback(current, total) for progress updates

        Returns:
            List of embedding vectors
        """
        embeddings: List[List[float]] = []
        cache = self.cache

        iterator = tqdm(
            texts,
            desc="Generating embeddings",
            disable=not show_progress,
        )

        for i, text in enumerate(iterator):
            # Try cache first if enabled
            if cache is not None:
                cached = cache.get(text)
                if cached is not None:
                    embeddings.append(cached)
                    if progress_callback:
                        progress_callback(i + 1, len(texts))
                    continue

            # Generate embedding
            embedding = self.embed(text)
            embeddings.append(embedding)

            # Cache if enabled
            if cache is not None:
                cache.set(text, embedding)

            if progress_callback:
                progress_callback(i + 1, len(texts))

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
