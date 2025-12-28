"""
Indexing models for AI Assistant RAG.
Defines schemas for content indexing operations.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    """Metadata for a document chunk."""

    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    source_path: str = Field(..., description="Source file path")
    chapter_path: str = Field(
        ..., description="Docusaurus URL path (e.g., /docs/module-1/intro)"
    )
    title: str = Field(..., description="Human-readable chapter title")
    section_title: Optional[str] = Field(
        default=None, description="Section heading within chapter"
    )
    start_token: int = Field(default=0, description="Start token position")
    end_token: int = Field(default=0, description="End token position")
    char_count: int = Field(default=0, description="Character count")

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "abc123def456",
                "source_path": "docs/physical-ai-robotics-course.md",
                "chapter_path": "/docs/physical-ai-robotics-course",
                "title": "Module 2: Digital Twin (Gazebo & Unity)",
                "section_title": "Introduction",
                "start_token": 0,
                "end_token": 512,
                "char_count": 2048,
            }
        }


class DocumentChunk(BaseModel):
    """Represents a chunk of indexed document content."""

    content: str = Field(..., description="The actual text content of the chunk")
    metadata: ChunkMetadata = Field(..., description="Chunk metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "A digital twin is a virtual representation of a physical object...",
                "metadata": {
                    "chunk_id": "abc123def456",
                    "source_path": "docs/physical-ai-robotics-course.md",
                    "chapter_path": "/docs/physical-ai-robotics-course",
                    "title": "Module 2: Digital Twin (Gazebo & Unity)",
                    "section_title": "Introduction",
                    "start_token": 0,
                    "end_token": 512,
                    "char_count": 2048,
                },
            }
        }


class IndexStatus(BaseModel):
    """Status of the content indexing process."""

    total_files: int = Field(default=0, description="Total files to be indexed")
    total_chunks: int = Field(default=0, description="Total chunks created")
    total_embeddings: int = Field(default=0, description="Total embeddings generated")
    total_points: int = Field(default=0, description="Total points in collection")
    elapsed_seconds: float = Field(default=0.0, description="Time taken for indexing")
    errors: list[str] = Field(default_factory=list, description="Error messages")

    class Config:
        json_schema_extra = {
            "example": {
                "total_files": 10,
                "total_chunks": 150,
                "total_embeddings": 150,
                "total_points": 150,
                "elapsed_seconds": 45.5,
                "errors": [],
            }
        }


class HealthStatus(BaseModel):
    """Health check response."""

    status: str = Field(
        ...,
        pattern="^(healthy|degraded|unhealthy)$",
        description="Overall system health status",
    )
    version: str = Field(..., description="API version")
    components: dict[str, Any] = Field(
        default_factory=dict, description="Individual component health statuses"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "components": {
                    "qdrant": {"status": "healthy", "points_count": 150},
                    "embeddings": {"status": "healthy", "provider": "text-embedding-3-small"},
                },
            }
        }


class ReindexRequest(BaseModel):
    """Request to trigger content re-indexing."""

    directory: str = Field(..., description="Directory path to index")
    base_url: str = Field(default="", description="Base URL prefix")
    force: bool = Field(
        default=False,
        description="If true, reindex even if content hasn't changed",
    )
    batch_size: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of documents to process in each batch",
    )


class SearchQuery(BaseModel):
    """Query for semantic search."""

    query: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="Search query",
    )
    selected_text: Optional[str] = Field(
        default=None, description="Selected text for context"
    )
    context_chapter: Optional[str] = Field(
        default=None, description="Filter results to specific chapter"
    )
    limit: int = Field(default=5, ge=1, le=20, description="Maximum results to return")
    threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Minimum relevance score"
    )


class SearchResult(BaseModel):
    """Result from semantic search."""

    chunk_id: str = Field(..., description="Unique chunk identifier")
    content: str = Field(..., description="Content excerpt")
    chapter_path: str = Field(..., description="Chapter URL path")
    title: str = Field(..., description="Chapter title")
    section_title: Optional[str] = Field(
        default=None, description="Section title"
    )
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Relevance score"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "abc123",
                "content": "A digital twin is a virtual representation...",
                "chapter_path": "/docs/uv-package-manager",
                "title": "Chapter 1: Getting Started with uv",
                "section_title": "Introduction",
                "relevance_score": 0.85,
            }
        }
