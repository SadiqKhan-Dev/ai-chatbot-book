"""
Qdrant client service for vector storage and retrieval.
Handles collection management and semantic search operations.
"""

import logging
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from ..core.config import get_settings
from ..models.indexing import ChunkMetadata

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for Qdrant vector database operations."""

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize Qdrant service."""
        settings = get_settings()

        self.url = url or settings.qdrant_url
        self.api_key = api_key or settings.qdrant_api_key
        self.collection_name = settings.qdrant_collection_name

        # Initialize client
        if self.api_key:
            self.client = QdrantClient(url=self.url, api_key=self.api_key)
        else:
            self.client = QdrantClient(url=self.url)

        logger.info(f"Qdrant client initialized: {self.url}")

    def ensure_collection(self, vector_size: int = 1536) -> bool:
        """
        Ensure the collection exists with proper configuration.

        Args:
            vector_size: Dimension of embedding vectors

        Returns:
            True if collection exists or was created successfully
        """
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return True

            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Created collection '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to ensure collection: {e}")
            raise

    def get_collection_info(self):
        """Get information about the current collection."""
        try:
            return self.client.get_collection(self.collection_name)
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return None

    def delete_collection(self) -> bool:
        """Delete the current collection."""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection '{self.collection_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            return False

    def upsert_points(
        self, points: list[PointStruct], batch_size: int = 100
    ) -> int:
        """
        Upload points to the collection.

        Args:
            points: List of PointStruct objects to upload
            batch_size: Number of points to upload per batch

        Returns:
            Total number of points uploaded
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                batch_size=batch_size,
            )
            logger.info(f"Upserted {len(points)} points to '{self.collection_name}'")
            return len(points)

        except Exception as e:
            logger.error(f"Failed to upsert points: {e}")
            raise

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float = 0.7,
    ) -> list[dict]:
        """
        Perform semantic search.

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum relevance score (0.0-1.0)

        Returns:
            List of search results with payload and scores
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
            )

            return [
                {
                    "id": r.id,
                    "score": r.score,
                    "payload": r.payload,
                }
                for r in results
            ]

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_points(
        self,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float = 0.0,
    ):
        """Search and return points with full metadata."""
        from qdrant_client.models import SearchRequest

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
            )
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def count_points(self) -> int:
        """Get the total number of points in the collection."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            logger.error(f"Failed to count points: {e}")
            return 0

    def delete_points(self, point_ids: list[int]) -> int:
        """Delete points by IDs."""
        try:
            from qdrant_client.models import PointsSelector, PointIdsList

            self.client.delete(
                collection_name=self.collection_name,
                points=PointIdsList(points=point_ids),
            )
            logger.info(f"Deleted {len(point_ids)} points")
            return len(point_ids)

        except Exception as e:
            logger.error(f"Failed to delete points: {e}")
            return 0

    def close(self):
        """Close the Qdrant client connection."""
        self.client.close()
