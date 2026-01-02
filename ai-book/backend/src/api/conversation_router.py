"""
Conversation router for managing chat history.
Provides endpoints for conversation CRUD operations.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..models.conversation import Conversation, ConversationSummary
from ..services.conversation_service import (
    ConversationManager,
    get_conversation_manager,
)

router = APIRouter(prefix="/api/v1/chat", tags=["Conversations"])


async def get_conversation_mgr() -> ConversationManager:
    """Dependency to get conversation manager."""
    return await get_conversation_manager()


@router.get("/conversations", response_model=list[ConversationSummary])
async def list_conversations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    manager: ConversationManager = Depends(get_conversation_mgr),
):
    """
    List all conversations for the current user.

    Returns conversation summaries without message content.
    """
    return await manager.list_conversations(
        user_id="anonymous",  # TODO: Replace with actual user from auth
        limit=limit,
        offset=offset,
    )


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    manager: ConversationManager = Depends(get_conversation_mgr),
):
    """
    Get a specific conversation with all messages.

    Returns full conversation including all messages.
    """
    conversation = await manager.get_conversation(
        conversation_id=conversation_id,
        user_id="anonymous",  # TODO: Replace with actual user from auth
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail=f"Conversation '{conversation_id}' not found",
        )

    return conversation


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    manager: ConversationManager = Depends(get_conversation_mgr),
):
    """
    Get messages from a conversation with pagination.

    Returns message list from a specific conversation.
    """
    conversation = await manager.get_conversation(
        conversation_id=conversation_id,
        user_id="anonymous",  # TODO: Replace with actual user from auth
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail=f"Conversation '{conversation_id}' not found",
        )

    messages = conversation.messages[offset : offset + limit]
    return {
        "conversation_id": conversation_id,
        "messages": messages,
        "total": len(conversation.messages),
        "limit": limit,
        "offset": offset,
    }


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    manager: ConversationManager = Depends(get_conversation_mgr),
):
    """
    Delete a conversation.

    Returns success status.
    """
    deleted = await manager.delete_conversation(
        conversation_id=conversation_id,
        user_id="anonymous",  # TODO: Replace with actual user from auth
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Conversation '{conversation_id}' not found",
        )

    return {"status": "deleted", "conversation_id": conversation_id}
