"""
Integration tests for chat API endpoints.
Tests full request/response cycles.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Note: These tests require mocking external services
# For full integration tests, use the test suite with real services


class TestChatEndpoint:
    """Integration tests for chat endpoint."""

    @pytest.fixture
    def mock_client(self, mocker):
        """Create test client with mocked dependencies."""
        # Mock embedding service
        mocker.patch(
            "src.services.embedding_service.OpenAIEmbeddingService.embed",
            return_value=[0.1] * 1536,
        )

        # Mock Qdrant search
        mocker.patch(
            "src.services.retrieval_service.QdrantService.search",
            return_value=[
                {
                    "id": "test-chunk",
                    "score": 0.9,
                    "payload": {
                        "content": "Test content",
                        "title": "Test Chapter",
                        "chapter_path": "/test/chapter.md",
                    },
                }
            ],
        )

        # Import and create app
        from src.main import app
        return TestClient(app)

    def test_health_endpoint(self, mock_client):
        """Test health check endpoint."""
        response = mock_client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint(self, mock_client):
        """Test root endpoint."""
        response = mock_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data


class TestSearchEndpoint:
    """Integration tests for search endpoint."""

    @pytest.fixture
    def def setup_client(self, mocker):
        """Set up test client with mocks."""
        from src.main import app
        return TestClient(app)

    def test_search_basic(self, setup_client):
        """Test basic search functionality."""
        response = setup_client.get("/api/v1/search?q=digital twin")
        # Should return 200 or 503 if Qdrant unavailable
        assert response.status_code in [200, 503]


class TestConversationEndpoints:
    """Integration tests for conversation endpoints."""

    @pytest.fixture
    def def setup_client(self):
        """Set up test client."""
        from src.main import app
        return TestClient(app)

    def test_list_conversations_empty(self, setup_client):
        """Test listing conversations when empty."""
        response = setup_client.get("/api/v1/chat/conversations")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_nonexistent_conversation(self, setup_client):
        """Test getting a conversation that doesn't exist."""
        response = setup_client.get("/api/v1/chat/conversations/nonexistent-id")
        assert response.status_code == 404
