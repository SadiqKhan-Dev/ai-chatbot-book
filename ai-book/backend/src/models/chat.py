"""
Chat models for AI Assistant RAG.
Defines request/response schemas for chat operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Citation(BaseModel):
    """Source citation for an AI response."""

    chunk_id: str = Field(..., description="Unique identifier for the source chunk")
    chapter_path: str = Field(
        ..., description="URL path to the source chapter"
    )
    title: str = Field(..., description="Title of the source chapter/section")
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Relevance score of this citation"
    )
    excerpt: Optional[str] = Field(
        default=None, description="Excerpt from the source content"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "abc123-def456",
                "chapter_path": "/docs/physical-ai-robotics-course",
                "title": "Module 2: Digital Twin (Gazebo & Unity)",
                "relevance_score": 0.92,
                "excerpt": "A digital twin is a virtual representation...",
            }
        }


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's question",
        examples=["What is a digital twin?"],
    )
    selected_text: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional selected text for context",
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="Optional conversation ID for continuity",
    )
    context_chapter: Optional[str] = Field(
        default=None,
        description="Optional chapter URL path to narrow context",
        examples=["/docs/digital-twin"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is a digital twin?",
                "selected_text": None,
                "conversation_id": None,
                "context_chapter": "/docs/digital-twin",
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str = Field(
        ..., description="AI-generated answer based on book content"
    )
    citations: list[Citation] = Field(
        default_factory=list, description="Source citations from book content"
    )
    conversation_id: str = Field(
        ..., description="Conversation ID for follow-up messages"
    )
    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score of the response",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "response": "A digital twin is a virtual representation of a physical object or system...",
                "citations": [
                    {
                        "chunk_id": "abc123-def456",
                        "chapter_path": "/docs/physical-ai-robotics-course",
                        "title": "Module 2: Digital Twin (Gazebo & Unity)",
                        "relevance_score": 0.92,
                    }
                ],
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "confidence_score": 0.95,
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str = Field(..., description="Error type")
    detail: Optional[str] = Field(default=None, description="Detailed error message")
    request_id: Optional[str] = Field(
        default=None, description="Request ID for debugging"
    )


class GroundingResult(BaseModel):
    """Result of grounding validation."""

    is_grounded: bool = Field(
        ..., description="Whether the response is grounded in source material"
    )
    max_relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Highest relevance score from retrieval"
    )
    passages_found: int = Field(
        ..., description="Number of relevant passages found"
    )
