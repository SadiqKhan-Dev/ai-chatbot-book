"""
Chat router for the AI assistant Q&A endpoint.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException

from ..models.chat import ChatRequest, ChatResponse, ErrorResponse
from ..services import ResponseGenerator

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# Global response generator (initialized on first request)
_response_generator: Optional[ResponseGenerator] = None


def get_response_generator() -> ResponseGenerator:
    """Get or create the response generator."""
    global _response_generator
    if _response_generator is None:
        _response_generator = ResponseGenerator()
    return _response_generator


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Generation error"},
    },
)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Ask a question about the book content.

    The AI will retrieve relevant passages from the indexed book content
    and generate a response based on those passages.

    - **query**: The user's question about the book content
    - **selected_text**: Optional selected text for additional context
    - **conversation_id**: Optional conversation ID for multi-turn chats
    - **context_chapter**: Optional chapter URL to narrow the search
    """
    try:
        generator = get_response_generator()

        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Generate response
        response = generator.generate_response(
            query=request.query,
            selected_text=request.selected_text,
            conversation_history=None,  # TODO: Implement conversation history
        )

        # Set conversation ID
        response.conversation_id = conversation_id

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}",
        )


@router.get("/{conversation_id}", response_model=ChatResponse)
async def get_conversation(conversation_id: str):
    """
    Get a conversation by ID.

    Returns the conversation metadata and messages.
    """
    # TODO: Implement conversation storage/retrieval
    raise HTTPException(
        status_code=501,
        detail="Conversation history not yet implemented",
    )


@router.get("/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: str):
    """
    Get all messages in a conversation.

    Returns the list of user queries and AI responses.
    """
    # TODO: Implement conversation storage/retrieval
    raise HTTPException(
        status_code=501,
        detail="Conversation history not yet implemented",
    )
