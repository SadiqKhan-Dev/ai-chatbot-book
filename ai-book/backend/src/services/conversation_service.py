"""
Conversation service for managing chat history and sessions.
Supports filesystem-based storage with optional Redis support.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid

from ..models.conversation import Conversation, Message, ConversationSummary


class ConversationStorage:
    """Base storage interface for conversations."""

    async def save(self, conversation: Conversation) -> None:
        """Save a conversation."""
        raise NotImplementedError

    async def load(self, conversation_id: str) -> Optional[Conversation]:
        """Load a conversation by ID."""
        raise NotImplementedError

    async def delete(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        raise NotImplementedError

    async def list(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> list[ConversationSummary]:
        """List conversations for a user."""
        raise NotImplementedError


class FilesystemStorage(ConversationStorage):
    """
    Filesystem-based conversation storage.
    Stores conversations as JSON files in a specified directory.
    """

    def __init__(self, storage_dir: str = "./conversations"):
        """
        Initialize filesystem storage.

        Args:
            storage_dir: Directory to store conversation JSON files
        """
        self._storage_dir = Path(storage_dir)
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_conversation_path(self, conversation_id: str) -> Path:
        """Get the file path for a conversation."""
        return self._storage_dir / f"{conversation_id}.json"

    async def save(self, conversation: Conversation) -> None:
        """Save conversation to JSON file."""
        path = self._get_conversation_path(conversation.id)
        data = conversation.to_dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    async def load(self, conversation_id: str) -> Optional[Conversation]:
        """Load conversation from JSON file."""
        path = self._get_conversation_path(conversation_id)
        if not path.exists():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Conversation.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    async def delete(self, conversation_id: str) -> bool:
        """Delete conversation file."""
        path = self._get_conversation_path(conversation_id)
        if path.exists():
            path.unlink()
            return True
        return False

    async def list(
        self, user_id: str = "anonymous", limit: int = 20, offset: int = 0
    ) -> list[ConversationSummary]:
        """List conversations from filesystem."""
        conversations: list[ConversationSummary] = []

        for path in self._storage_dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if data.get("user_id") != user_id:
                    continue

                messages = data.get("messages", [])
                last_preview = None
                if messages:
                    last_msg = messages[-1]
                    last_preview = last_msg.get("content", "")[:100]

                conversations.append(
                    ConversationSummary(
                        id=data.get("id", path.stem),
                        title=data.get("title", "New Conversation"),
                        created_at=datetime.fromisoformat(data.get("created_at")),
                        updated_at=datetime.fromisoformat(data.get("updated_at")),
                        message_count=len(messages),
                        last_message_preview=last_preview,
                    )
                )
            except (json.JSONDecodeError, KeyError, OSError):
                continue

        # Sort by updated_at descending
        conversations.sort(key=lambda c: c.updated_at, reverse=True)

        # Apply pagination
        return conversations[offset : offset + limit]


class ConversationManager:
    """
    Manages conversation lifecycle and storage.

    Responsibilities:
    - Create new conversations
    - Load/save conversations
    - Add messages to conversations
    - Generate conversation titles
    - List user's conversations
    """

    def __init__(self, storage: Optional[ConversationStorage] = None):
        """
        Initialize conversation manager.

        Args:
            storage: Storage backend (defaults to filesystem)
        """
        self._storage = storage or FilesystemStorage()

    async def create_conversation(self, user_id: str = "anonymous") -> Conversation:
        """
        Create a new conversation.

        Args:
            user_id: User identifier

        Returns:
            New Conversation instance
        """
        conversation = Conversation(user_id=user_id)
        await self._storage.save(conversation)
        return conversation

    async def get_conversation(
        self, conversation_id: str, user_id: str = "anonymous"
    ) -> Optional[Conversation]:
        """
        Get an existing conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User identifier for validation

        Returns:
            Conversation if found and owned by user, None otherwise
        """
        conversation = await self._storage.load(conversation_id)
        if conversation and conversation.user_id == user_id:
            return conversation
        return None

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        citations: list[dict] = None,
        user_id: str = "anonymous",
    ) -> Conversation:
        """
        Add a message to an existing conversation.

        Args:
            conversation_id: Conversation ID
            role: Message role (user/assistant)
            content: Message content
            citations: Optional citations for assistant messages
            user_id: User identifier

        Returns:
            Updated Conversation
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            # Create new conversation if not found
            conversation = Conversation(user_id=user_id)

        conversation.add_message(role=role, content=content, citations=citations)
        await self._storage.save(conversation)
        return conversation

    async def create_or_get_conversation(
        self, conversation_id: Optional[str], user_id: str = "anonymous"
    ) -> Conversation:
        """
        Get existing conversation or create new one.

        Args:
            conversation_id: Optional conversation ID (creates new if None)
            user_id: User identifier

        Returns:
            Conversation instance
        """
        if conversation_id:
            existing = await self.get_conversation(conversation_id, user_id)
            if existing:
                return existing

        return await self.create_conversation(user_id)

    async def delete_conversation(
        self, conversation_id: str, user_id: str = "anonymous"
    ) -> bool:
        """
        Delete a conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User identifier

        Returns:
            True if deleted, False if not found
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            return False

        return await self._storage.delete(conversation_id)

    async def list_conversations(
        self,
        user_id: str = "anonymous",
        limit: int = 20,
        offset: int = 0,
    ) -> list[ConversationSummary]:
        """
        List conversations for a user.

        Args:
            user_id: User identifier
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of conversation summaries
        """
        return await self._storage.list(user_id=user_id, limit=limit, offset=offset)

    def generate_title(self, first_message: str) -> str:
        """
        Generate a title from the first message.

        Args:
            first_message: First user message

        Returns:
            Generated title
        """
        # Simple title generation: truncate to first meaningful words
        if not first_message:
            return "New Conversation"

        # Remove common prefixes
        cleaned = first_message.strip()
        prefixes = ["what is", "how do", "tell me", "explain", "what does"]
        for prefix in prefixes:
            if cleaned.lower().startswith(prefix):
                cleaned = cleaned[len(prefix) :].strip()

        # Truncate to 50 characters
        if len(cleaned) > 50:
            return cleaned[:50].strip() + "..."
        return cleaned


# Convenience function
async def get_conversation_manager(
    storage_dir: str = "./conversations",
) -> ConversationManager:
    """
    Get a conversation manager with filesystem storage.

    Args:
        storage_dir: Directory for conversation storage

    Returns:
        ConversationManager instance
    """
    storage = FilesystemStorage(storage_dir)
    return ConversationManager(storage)
