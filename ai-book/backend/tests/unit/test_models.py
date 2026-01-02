"""
Unit tests for Pydantic models.
Tests validation, serialization, and model behavior.
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models.chat import ChatRequest, ChatResponse, Citation
from src.models.conversation import Conversation, Message
from src.models.indexing import IndexStatus, ReindexRequest


class TestCitationModel:
    """Tests for Citation model."""

    def test_citation_create(self):
        """Test basic citation creation."""
        citation = Citation(
            chunk_id="test-chunk-123",
            title="Chapter 1: Introduction",
            chapter_path="/docs/chapter1.md",
            relevance_score=0.95,
        )
        assert citation.chunk_id == "test-chunk-123"
        assert citation.title == "Chapter 1: Introduction"
        assert citation.relevance_score == 0.95

    def test_citation_serialization(self):
        """Test citation to dict serialization."""
        citation = Citation(
            chunk_id="test-chunk-456",
            title="Test Chapter",
            chapter_path="/test/chapter.md",
            relevance_score=0.85,
        )
        data = citation.model_dump()
        assert data["chunk_id"] == "test-chunk-456"
        assert data["title"] == "Test Chapter"
        assert data["relevance_score"] == 0.85

    def test_citation_with_excerpt(self):
        """Test citation with optional excerpt."""
        citation = Citation(
            chunk_id="test-chunk-789",
            title="Chapter with Excerpt",
            chapter_path="/docs/excerpt.md",
            relevance_score=0.92,
            excerpt="This is an excerpt from the source...",
        )
        assert citation.excerpt == "This is an excerpt from the source..."


class TestChatRequestModel:
    """Tests for ChatRequest model."""

    def test_chat_request_create(self):
        """Test basic chat request creation."""
        request = ChatRequest(query="What is a digital twin?")
        assert request.query == "What is a digital twin?"
        assert request.conversation_id is None
        assert request.selected_text is None

    def test_chat_request_with_context(self):
        """Test chat request with selected text context."""
        request = ChatRequest(
            query="Explain this concept",
            selected_text="Digital twins are virtual representations...",
        )
        assert request.selected_text == "Digital twins are virtual representations..."

    def test_chat_request_with_conversation(self):
        """Test chat request with conversation ID."""
        request = ChatRequest(
            query="Continue the explanation",
            conversation_id="conv-123",
        )
        assert request.conversation_id == "conv-123"


class TestChatResponseModel:
    """Tests for ChatResponse model."""

    def test_response_create(self):
        """Test basic response creation."""
        response = ChatResponse(
            response="A digital twin is...",
            citations=[],
            conversation_id="conv-123",
        )
        assert response.response == "A digital twin is..."
        assert response.citations == []
        assert response.conversation_id == "conv-123"

    def test_response_with_citations(self):
        """Test response with citations."""
        citations = [
            Citation(
                chunk_id="chunk-1",
                title="Chapter 1",
                chapter_path="/ch1.md",
                relevance_score=0.9,
            )
        ]
        response = ChatResponse(
            response="Based on the book...",
            citations=citations,
            conversation_id="conv-456",
            confidence_score=0.85,
        )
        assert len(response.citations) == 1
        assert response.confidence_score == 0.85

    def test_response_without_confidence(self):
        """Test response without optional confidence score."""
        response = ChatResponse(
            response="Simple answer",
            citations=[],
            conversation_id="conv-789",
        )
        assert response.confidence_score is None


class TestMessageModel:
    """Tests for Message model."""

    def test_message_create(self):
        """Test basic message creation."""
        message = Message(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"
        assert message.id is not None
        assert message.created_at is not None

    def test_assistant_message_with_citations(self):
        """Test assistant message with citations."""
        message = Message(
            role="assistant",
            content="The answer is 42.",
            citations=[{"chunk_id": "abc", "title": "Test"}],
        )
        assert len(message.citations) == 1


class TestConversationModel:
    """Tests for Conversation model."""

    def test_conversation_create(self):
        """Test basic conversation creation."""
        conv = Conversation()
        assert conv.id is not None
        assert conv.message_count == 0
        assert conv.title == "New Conversation"

    def test_conversation_add_message(self):
        """Test adding messages to conversation."""
        conv = Conversation()
        conv.add_message(role="user", content="What is AI?")
        conv.add_message(role="assistant", content="AI is...")

        assert conv.message_count == 2
        assert conv.messages[0].role == "user"
        assert conv.messages[1].role == "assistant"

    def test_conversation_title_generation(self):
        """Test automatic title generation from first message."""
        conv = Conversation()
        conv.add_message(role="user", content="What is machine learning?")

        assert conv.title == "What is machine learning?"

    def test_conversation_title_truncation(self):
        """Test title truncation for long messages."""
        conv = Conversation()
        long_message = "This is a very long first message that exceeds fifty characters"
        conv.add_message(role="user", content=long_message)

        # Title should be truncated to 50 chars
        assert len(conv.title) <= 53
        assert conv.title.startswith("This is a very long first message that")

    def test_conversation_serialization(self):
        """Test conversation serialization to dict."""
        conv = Conversation()
        conv.add_message(role="user", content="Test")
        conv.add_message(role="assistant", content="Response")

        data = conv.to_dict()
        assert "id" in data
        assert "messages" in data
        assert len(data["messages"]) == 2
        assert data["messages"][0]["content"] == "Test"

    def test_conversation_deserialization(self):
        """Test conversation deserialization from dict."""
        conv = Conversation()
        conv.add_message(role="user", content="Test message")

        data = conv.to_dict()
        restored = Conversation.from_dict(data)

        assert restored.id == conv.id
        assert restored.message_count == conv.message_count


class TestIndexStatusModel:
    """Tests for IndexStatus model."""

    def test_index_status_create(self):
        """Test basic index status creation."""
        status = IndexStatus(
            total_files=10,
            total_chunks=100,
            total_embeddings=100,
            total_points=100,
            elapsed_seconds=45.5,
        )
        assert status.total_files == 10
        assert status.total_chunks == 100
        assert status.elapsed_seconds == 45.5

    def test_index_status_defaults(self):
        """Test index status default values."""
        status = IndexStatus()
        assert status.total_files == 0
        assert status.total_chunks == 0
        assert status.errors == []

    def test_index_status_with_errors(self):
        """Test index status with error messages."""
        status = IndexStatus(
            total_files=5,
            errors=["Error in file1.md", "Error in file2.md"],
        )
        assert len(status.errors) == 2

    def test_index_status_serialization(self):
        """Test index status serialization."""
        status = IndexStatus(
            total_files=10,
            total_chunks=150,
            total_embeddings=150,
            total_points=150,
            elapsed_seconds=60.0,
        )
        data = status.model_dump()
        assert data["total_files"] == 10
        assert data["total_chunks"] == 150


class TestReindexRequestModel:
    """Tests for ReindexRequest model."""

    def test_reindex_request_defaults(self):
        """Test reindex request default values."""
        request = ReindexRequest(directory="/docs")
        assert request.base_url == ""
        assert request.force is False
        assert request.batch_size == 10

    def test_reindex_request_custom(self):
        """Test reindex request with custom values."""
        request = ReindexRequest(
            directory="/docs",
            base_url="/book",
            force=True,
            batch_size=20,
        )
        assert request.force is True
        assert request.batch_size == 20
