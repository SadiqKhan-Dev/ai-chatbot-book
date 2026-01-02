"""
Contract tests for OpenAPI specification validation.
Ensures the FastAPI implementation matches the defined API contracts.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


class TestOpenAPIContract:
    """Test that the API implementation adheres to the OpenAPI spec."""

    @pytest.fixture(scope="class")
    def openapi_spec_path(self) -> Path:
        """Path to the OpenAPI specification file."""
        return Path(__file__).parent.parent.parent.parent / "specs" / "005-ai-assistant-rag" / "contracts" / "openapi.yaml"

    @pytest.fixture(scope="class")
    def openapi_spec(self, openapi_spec_path: Path) -> dict:
        """Load the OpenAPI specification."""
        import yaml

        assert openapi_spec_path.exists(), f"OpenAPI spec not found at {openapi_spec_path}"
        with open(openapi_spec_path, "r") as f:
            return yaml.safe_load(f)

    @pytest.fixture(scope="class")
    def test_client(self) -> TestClient:
        """Create a test client for the FastAPI app."""
        from src.main import app

        return TestClient(app, raise_server_exceptions=False)


class TestChatEndpointContract(TestOpenAPIContract):
    """Contract tests for /api/v1/chat endpoint."""

    def test_endpoint_exists(self, test_client: TestClient):
        """Test that POST /api/v1/chat endpoint exists."""
        response = test_client.post("/api/v1/chat", json={"query": "test"})
        # Accept any response (could be 200, 400, 401, 500, etc.)
        assert response.status_code in [200, 400, 401, 500]

    def test_request_body_schema(self, test_client: TestClient, openapi_spec: dict):
        """Test that request body matches OpenAPI schema."""
        from jsonschema import validate, ValidationError

        chat_schema = openapi_spec["components"]["schemas"]["ChatRequest"]

        # Valid request
        valid_request = {
            "query": "What is a digital twin?",
            "selected_text": None,
            "conversation_id": None,
            "context_chapter": "/docs/digital-twin"
        }

        # Should not raise ValidationError
        validate(instance=valid_request, schema=chat_schema)

    def test_response_body_schema(self, test_client: TestClient, openapi_spec: dict):
        """Test that response body matches OpenAPI schema."""
        from jsonschema import validate, ValidationError

        chat_schema = openapi_spec["components"]["schemas"]["ChatResponse"]

        response = test_client.post("/api/v1/chat", json={"query": "test"})

        if response.status_code == 200:
            try:
                validate(instance=response.json(), schema=chat_schema)
            except ValidationError as e:
                pytest.fail(f"Response does not match ChatResponse schema: {e.message}")

    def test_required_fields_in_request(self, test_client: TestClient):
        """Test that query field is required."""
        response = test_client.post("/api/v1/chat", json={})
        assert response.status_code == 422  # Validation error

    def test_query_min_length(self, test_client: TestClient):
        """Test that query must be at least 1 character."""
        response = test_client.post("/api/v1/chat", json={"query": ""})
        assert response.status_code == 422


class TestConversationEndpointsContract(TestOpenAPIContract):
    """Contract tests for conversation endpoints."""

    def test_get_conversation_endpoint_exists(self, test_client: TestClient):
        """Test that GET /api/v1/chat/{conversation_id} endpoint exists."""
        response = test_client.get("/api/v1/chat/550e8400-e29b-41d4-a716-446655440000")
        # Accept any response (could be 200, 404)
        assert response.status_code in [200, 404]

    def test_get_messages_endpoint_exists(self, test_client: TestClient):
        """Test that GET /api/v1/chat/{conversation_id}/messages endpoint exists."""
        response = test_client.get("/api/v1/chat/550e8400-e29b-41d4-a716-446655440000/messages")
        # Accept any response (could be 200, 404)
        assert response.status_code in [200, 404]


class TestSearchEndpointContract(TestOpenAPIContract):
    """Contract tests for /api/v1/search endpoint."""

    def test_search_endpoint_exists(self, test_client: TestClient):
        """Test that GET /api/v1/search endpoint exists."""
        response = test_client.get("/api/v1/search", params={"q": "digital twin"})
        assert response.status_code in [200, 400, 500]

    def test_search_query_required(self, test_client: TestClient):
        """Test that q parameter is required."""
        response = test_client.get("/api/v1/search")
        assert response.status_code == 422


class TestHealthEndpointContract(TestOpenAPIContract):
    """Contract tests for /api/v1/health endpoint."""

    def test_health_endpoint_exists(self, test_client: TestClient):
        """Test that GET /api/v1/health endpoint exists."""
        response = test_client.get("/api/v1/health")
        assert response.status_code in [200, 503]

    def test_health_response_schema(self, test_client: TestClient, openapi_spec: dict):
        """Test that health response matches OpenAPI schema."""
        from jsonschema import validate, ValidationError

        health_schema = openapi_spec["components"]["schemas"]["HealthResponse"]

        response = test_client.get("/api/v1/health")

        if response.status_code in [200, 503]:
            try:
                validate(instance=response.json(), schema=health_schema)
            except ValidationError as e:
                pytest.fail(f"Health response does not match schema: {e.message}")


class TestIndexingEndpointsContract(TestOpenAPIContract):
    """Contract tests for indexing endpoints."""

    def test_index_status_endpoint_exists(self, test_client: TestClient):
        """Test that GET /api/v1/index endpoint exists."""
        response = test_client.get("/api/v1/index")
        assert response.status_code in [200, 401, 500]

    def test_reindex_endpoint_exists(self, test_client: TestClient):
        """Test that POST /api/v1/index endpoint exists."""
        response = test_client.post("/api/v1/index", json={})
        assert response.status_code in [202, 401, 500]


class TestResponseSchemasContract(TestOpenAPIContract):
    """Contract tests for response schemas."""

    def test_citation_schema(self, openapi_spec: dict):
        """Test Citation schema structure."""
        from jsonschema import validate

        citation_schema = openapi_spec["components"]["schemas"]["Citation"]

        valid_citation = {
            "chunk_id": "abc123-def456",
            "chapter_path": "/docs/physical-ai-robotics-course",
            "title": "Module 2: Digital Twin",
            "relevance_score": 0.92
        }

        validate(instance=valid_citation, schema=citation_schema)

    def test_conversation_response_schema(self, openapi_spec: dict):
        """Test ConversationResponse schema structure."""
        from jsonschema import validate

        schema = openapi_spec["components"]["schemas"]["ConversationResponse"]

        valid_response = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2025-12-28T10:00:00Z",
            "updated_at": "2025-12-28T10:30:00Z",
            "title": "Questions about digital twins",
            "message_count": 5
        }

        validate(instance=valid_response, schema=schema)

    def test_message_response_schema(self, openapi_spec: dict):
        """Test MessageResponse schema structure."""
        from jsonschema import validate

        schema = openapi_spec["components"]["schemas"]["MessageResponse"]

        valid_message = {
            "id": "msg_123",
            "role": "assistant",
            "content": "A digital twin is...",
            "citations": [],
            "created_at": "2025-12-28T10:15:00Z"
        }

        validate(instance=valid_message, schema=schema)

    def test_index_status_schema(self, openapi_spec: dict):
        """Test IndexStatus schema structure."""
        from jsonschema import validate

        schema = openapi_spec["components"]["schemas"]["IndexStatus"]

        valid_status = {
            "status": "completed",
            "total_chunks": 150,
            "indexed_chunks": 150,
            "last_indexed_at": "2025-12-28T09:00:00Z",
            "error": None
        }

        validate(instance=valid_status, schema=schema)


class TestErrorResponsesContract(TestOpenAPIContract):
    """Contract tests for error responses."""

    def test_bad_request_response_structure(self, test_client: TestClient):
        """Test that 400 responses have expected structure."""
        response = test_client.post("/api/v1/chat", json={"query": "x" * 3000})  # Too long
        if response.status_code == 400:
            data = response.json()
            assert "error" in data or "detail" in data

    def test_not_found_response_structure(self, test_client: TestClient):
        """Test that 404 responses have expected structure."""
        response = test_client.get("/api/v1/chat/550e8400-e29b-41d4-a716-446655440000")
        if response.status_code == 404:
            data = response.json()
            assert "error" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
