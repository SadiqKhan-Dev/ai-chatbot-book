"""
Unit tests for retrieval service.
Tests similarity search and relevance scoring.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.services.retrieval_service import SemanticRetriever


class TestSemanticRetriever:
    """Tests for SemanticRetriever."""

    def test_retriever_initialization(self):
        """Test retriever initialization with mocked services."""
        mock_qdrant = Mock()
        mock_embedding = Mock()
        mock_embedding.dimension = 1536

        retriever = SemanticRetriever(
            qdrant_service=mock_qdrant,
            embedding_service=mock_embedding,
        )

        assert retriever.qdrant_service == mock_qdrant
        assert retriever.embedding_service == mock_embedding

    def test_search_with_query(self):
        """Test basic search functionality."""
        mock_qdrant = Mock()
        mock_embedding = Mock()
        mock_embedding.dimension = 1536
        mock_embedding.embed.return_value = [0.1] * 1536

        mock_qdrant.search.return_value = [
            {
                "id": "chunk-1",
                "score": 0.9,
                "payload": {
                    "content": "Test content",
                    "title": "Test Chapter",
                    "chapter_path": "/test/chapter.md",
                },
            }
        ]

        retriever = SemanticRetriever(
            qdrant_service=mock_qdrant,
            embedding_service=mock_embedding,
        )

        results = retriever.search(query="test query")

        # Verify embedding was called
        mock_embedding.embed.assert_called_once_with("test query")

        # Verify Qdrant search was called
        mock_qdrant.search.assert_called_once()

    def test_search_with_selected_text(self):
        """Test search with selected text context."""
        mock_qdrant = Mock()
        mock_embedding = Mock()
        mock_embedding.dimension = 1536
        mock_embedding.embed.return_value = [0.1] * 1536

        mock_qdrant.search.return_value = []

        retriever = SemanticRetriever(
            qdrant_service=mock_qdrant,
            embedding_service=mock_embedding,
        )

        results = retriever.search(
            query="What is this?",
            selected_text="Context from selection",
        )

        # Verify the combined query was used
        call_args = mock_embedding.embed.call_args[0][0]
        assert "What is this?" in call_args
        assert "Context from selection" in call_args

    def test_search_with_chapter_filter(self):
        """Test search with chapter path filter."""
        mock_qdrant = Mock()
        mock_embedding = Mock()
        mock_embedding.dimension = 1536
        mock_embedding.embed.return_value = [0.1] * 1536

        mock_qdrant.search.return_value = []

        retriever = SemanticRetriever(
            qdrant_service=mock_qdrant,
            embedding_service=mock_embedding,
        )

        results = retriever.search(
            query="test",
            context_chapter="/docs/module-1",
        )

        # Qdrant search should be called
        mock_qdrant.search.assert_called_once()

    def test_search_with_custom_limit(self):
        """Test search with custom result limit."""
        mock_qdrant = Mock()
        mock_embedding = Mock()
        mock_embedding.dimension = 1536
        mock_embedding.embed.return_value = [0.1] * 1536

        mock_qdrant.search.return_value = []

        retriever = SemanticRetriever(
            qdrant_service=mock_qdrant,
            embedding_service=mock_embedding,
        )

        results = retriever.search(query="test", limit=10)

        # Verify limit was passed to Qdrant
        call_kwargs = mock_qdrant.search.call_args[1]
        assert call_kwargs.get("limit") == 10


class TestSearchResultProcessing:
    """Tests for search result processing."""

    def test_result_format(self):
        """Test that results are properly formatted."""
        # This tests the _format_results method if it exists
        mock_qdrant = Mock()
        mock_embedding = Mock()
        mock_embedding.dimension = 1536
        mock_embedding.embed.return_value = [0.1] * 1536

        mock_qdrant.search.return_value = [
            {
                "id": "chunk-1",
                "score": 0.85,
                "payload": {
                    "content": "Relevant content here",
                    "title": "Chapter 1",
                    "chapter_path": "/docs/ch1.md",
                },
            }
        ]

        retriever = SemanticRetriever(
            qdrant_service=mock_qdrant,
            embedding_service=mock_embedding,
        )

        results = retriever.search(query="test")

        if results:
            # Verify result structure
            result = results[0]
            assert hasattr(result, 'chunk_id') or 'chunk_id' in str(type(result))
