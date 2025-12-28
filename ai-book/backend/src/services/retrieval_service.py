"""
Retrieval service for semantic search operations.
Handles querying the vector store and result processing.
"""

import logging
from typing import Optional

from ..core.config import get_settings
from ..models.chat import Citation
from ..models.indexing import SearchResult
from ..services import QdrantService, create_embedding_service

logger = logging.getLogger(__name__)


class SemanticRetriever:
    """Service for semantic retrieval from the vector store."""

    def __init__(
        self,
        qdrant_service: Optional[QdrantService] = None,
        embedding_service=None,
    ):
        """Initialize the semantic retriever."""
        settings = get_settings()

        self.qdrant_service = qdrant_service or QdrantService()
        self.embedding_service = embedding_service or create_embedding_service()

        self.relevance_threshold = settings.retrieval_relevance_threshold
        self.max_passages = settings.max_retrieved_passages

        logger.info("SemanticRetriever initialized")

    def search(
        self,
        query: str,
        selected_text: Optional[str] = None,
        context_chapter: Optional[str] = None,
        limit: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> list[SearchResult]:
        """
        Perform semantic search for relevant passages.

        Args:
            query: User's search query
            selected_text: Optional selected text for context
            context_chapter: Optional chapter path to narrow search
            limit: Maximum number of results (overrides setting)
            threshold: Minimum relevance score (overrides setting)

        Returns:
            List of SearchResult objects with passages and metadata
        """
        # Build enhanced query with selected text
        search_query = query
        if selected_text:
            search_query = f"{query}\n\nContext: {selected_text}"

        # Generate query embedding
        query_embedding = self.embedding_service.embed(search_query)

        # Set search parameters
        score_threshold = threshold or self.relevance_threshold
        result_limit = limit or self.max_passages

        # Search Qdrant
        results = self.qdrant_service.search(
            query_vector=query_embedding,
            limit=result_limit,
            score_threshold=score_threshold,
        )

        # Filter by chapter if specified
        if context_chapter:
            results = [
                r for r in results
                if r.get("payload", {}).get("chapter_path", "").startswith(context_chapter)
            ]

        # Convert to SearchResult objects
        search_results: list[SearchResult] = []

        for r in results:
            payload = r.get("payload", {})
            search_results.append(
                SearchResult(
                    chunk_id=payload.get("chunk_id", ""),
                    content=payload.get("content", ""),
                    chapter_path=payload.get("chapter_path", ""),
                    title=payload.get("title", ""),
                    section_title=payload.get("section_title", ""),
                    relevance_score=r.get("score", 0.0),
                )
            )

        logger.info(f"Retrieved {len(search_results)} passages for query: {query[:50]}...")

        return search_results

    def search_with_citations(
        self,
        query: str,
        selected_text: Optional[str] = None,
        context_chapter: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[Citation]:
        """
        Perform search and return Citation objects.

        Args:
            query: User's search query
            selected_text: Optional selected text for context
            context_chapter: Optional chapter path to narrow search
            limit: Maximum number of results

        Returns:
            List of Citation objects
        """
        results = self.search(
            query=query,
            selected_text=selected_text,
            context_chapter=context_chapter,
            limit=limit,
        )

        citations: list[Citation] = []

        for r in results:
            # Create excerpt from content (first 200 chars)
            excerpt = r.content[:200] + "..." if len(r.content) > 200 else r.content

            citations.append(
                Citation(
                    chunk_id=r.chunk_id,
                    chapter_path=r.chapter_path,
                    title=r.title or r.section_title,
                    relevance_score=r.relevance_score,
                    excerpt=excerpt,
                )
            )

        return citations

    def get_relevant_passages(
        self,
        query: str,
        selected_text: Optional[str] = None,
        max_passages: Optional[int] = None,
    ) -> tuple[list[str], list[Citation]]:
        """
        Get passages and citations for RAG generation.

        Args:
            query: User's question
            selected_text: Optional selected text context
            max_passages: Maximum number of passages to retrieve

        Returns:
            Tuple of (list of passage texts, list of citations)
        """
        limit = max_passages or self.max_passages

        citations = self.search_with_citations(
            query=query,
            selected_text=selected_text,
            limit=limit,
        )

        passages = [c.excerpt or "" for c in citations]

        return passages, citations

    def check_query_grounding(self, query: str) -> tuple[bool, float]:
        """
        Check if a query can be grounded in the knowledge base.

        Args:
            query: User's question

        Returns:
            Tuple of (is_grounded, max_relevance_score)
        """
        # Search with low threshold to find best match
        results = self.search(query=query, threshold=0.0, limit=1)

        if not results:
            return False, 0.0

        max_score = results[0].relevance_score
        is_grounded = max_score >= self.relevance_threshold

        return is_grounded, max_score

    def get_count(self) -> int:
        """Get total number of indexed passages."""
        return self.qdrant_service.count_points()

    def close(self):
        """Clean up resources."""
        self.qdrant_service.close()
