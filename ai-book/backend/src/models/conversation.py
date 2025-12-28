"""
Conversation models for AI Assistant RAG.
Defines schemas for conversation history and messages.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Individual message in a conversation."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    role: str = Field(
        ...,
        pattern="^(user|assistant|system)$",
        description="Message role: user, assistant, or system",
    )
    content: str = Field(..., description="Message content")
    citations: list[dict] = Field(
        default_factory=list, description="Source citations for assistant messages"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg_123",
                "role": "assistant",
                "content": "A digital twin is a virtual representation...",
                "citations": [{"chunk_id": "abc123", "title": "Module 2"}],
                "created_at": "2025-12-28T10:15:00Z",
            }
        }


class Conversation(BaseModel):
    """Conversation session containing multiple messages."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str = Field(
        default="anonymous", description="User identifier (session-based)"
    )
    title: str = Field(
        default="New Conversation",
        description="Generated title from first query",
    )
    messages: list[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def message_count(self) -> int:
        """Get the number of messages in the conversation."""
        return len(self.messages)

    def add_message(self, role: str, content: str, citations: list[dict] = None):
        """Add a message to the conversation."""
        message = Message(role=role, content=content, citations=citations or [])
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

        # Update title from first user message
        if not self.title or self.title == "New Conversation":
            if role == "user" and len(content) > 0:
                # Truncate to first 50 characters for title
                self.title = content[:50].strip() + "..." if len(content) > 50 else content.strip()

    def get_recent_messages(self, count: int = 5) -> list[Message]:
        """Get the most recent messages."""
        return self.messages[-count:] if count > 0 else self.messages

    def to_dict(self) -> dict:
        """Convert conversation to dictionary for storage."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "messages": [m.model_dump() for m in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        """Create conversation from dictionary."""
        messages = [Message(**m) for m in data.get("messages", [])]
        return cls(
            id=data.get("id", str(uuid4())),
            user_id=data.get("user_id", "anonymous"),
            title=data.get("title", "New Conversation"),
            messages=messages,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )


class ConversationSummary(BaseModel):
    """Summary of a conversation for list views."""

    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    last_message_preview: Optional[str] = None
