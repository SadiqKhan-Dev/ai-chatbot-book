"""
Generation service for RAG response generation.
Handles LLM calls and response formatting.
"""

import logging
from typing import Optional

from openai import OpenAI

from ..core.config import get_settings
from ..models.chat import ChatResponse, Citation
from .retrieval_service import SemanticRetriever

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Service for generating AI responses using RAG."""

    def __init__(
        self,
        openai_client: Optional[OpenAI] = None,
        retriever: Optional[SemanticRetriever] = None,
    ):
        """Initialize the response generator."""
        settings = get_settings()

        self.retriever = retriever or SemanticRetriever()
        self.chat_model = settings.openai_chat_model

        # Initialize OpenAI client
        if openai_client:
            self.client = openai_client
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)

        self.max_context_tokens = settings.max_context_tokens

        logger.info(f"ResponseGenerator initialized with model: {self.chat_model}")

    def generate_response(
        self,
        query: str,
        selected_text: Optional[str] = None,
        conversation_history: Optional[list[dict]] = None,
    ) -> ChatResponse:
        """
        Generate a response to a user query using RAG.

        Args:
            query: User's question
            selected_text: Optional selected text for context
            conversation_history: Optional previous messages

        Returns:
            ChatResponse with answer and citations
        """
        # Retrieve relevant passages
        passages, citations = self.retriever.get_relevant_passages(
            query=query,
            selected_text=selected_text,
        )

        # Check grounding
        is_grounded, max_score = self.retriever.check_query_grounding(query)

        if not is_grounded or not passages:
            # Return fallback response for out-of-scope queries
            return self._generate_fallback_response(
                query=query,
                citations=citations,
                max_score=max_score,
            )

        # Build context from passages
        context = self._build_context(passages)

        # Build messages
        messages = self._build_messages(
            query=query,
            context=context,
            selected_text=selected_text,
            history=conversation_history,
        )

        # Generate response
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more focused answers
                max_tokens=1000,
            )

            answer = response.choices[0].message.content or ""

            # Calculate confidence based on retrieval scores
            avg_score = sum(c.relevance_score for c in citations) / len(citations)
            confidence = min(avg_score * 1.1, 1.0)  # Slight boost, capped at 1.0

            return ChatResponse(
                response=answer,
                citations=citations,
                conversation_id="",  # Set by caller
                confidence_score=confidence,
            )

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_error_response(query, citations)

    def _build_context(self, passages: list[str]) -> str:
        """Build context string from retrieved passages."""
        context_parts = []

        for i, passage in enumerate(passages, 1):
            context_parts.append(f"[Passage {i}]\n{passage}")

        return "\n\n".join(context_parts)

    def _build_messages(
        self,
        query: str,
        context: str,
        selected_text: Optional[str],
        history: Optional[list[dict]],
    ) -> list[dict]:
        """Build messages for the LLM."""
        messages: list[dict] = []

        # System prompt
        system_prompt = """You are a helpful AI assistant for a technical book about Physical AI and Robotics.
Your role is to answer questions based ONLY on the provided book content.

Guidelines:
1. Answer based on the provided context passages
2. If the question cannot be answered from the context, say so clearly
3. Cite sources by mentioning the relevant chapter/section when possible
4. Keep answers concise and focused
5. Use code examples from the context when relevant
6. If selected text is provided, use it as additional context

Current context from the book:"""

        messages.append({
            "role": "system",
            "content": f"{system_prompt}\n\n{context}",
        })

        # Add selected text as user message context if provided
        if selected_text:
            messages.append({
                "role": "user",
                "content": f"Selected text for context:\n\n{selected_text}\n\nMy question: {query}",
            })
        else:
            messages.append({
                "role": "user",
                "content": query,
            })

        # Add conversation history (most recent first, limit to 5)
        if history:
            # Take last 5 messages, alternating user/assistant
            for msg in history[-5:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

        return messages

    def _generate_fallback_response(
        self,
        query: str,
        citations: list[Citation],
        max_score: float,
    ) -> ChatResponse:
        """Generate a fallback response for unanswerable queries."""
        suggestions = self._generate_suggestions(query, citations)

        if citations:
            # Partial match - use best available
            partial_context = "\n".join([
                f"- {c.title}: {c.excerpt[:100]}..." if c.excerpt else ""
                for c in citations[:3]
            ])

            response = (
                "I found some related information but may not have a complete answer:\n\n"
                f"{partial_context}\n\n"
                f"{suggestions}"
            )
        else:
            # No relevant content found
            response = (
                "I don't have enough information in the book to answer this question. "
                "The question appears to be outside the scope of the current content.\n\n"
                f"{suggestions}"
            )

        return ChatResponse(
            response=response,
            citations=citations,
            conversation_id="",
            confidence_score=max_score if citations else 0.0,
        )

    def _generate_suggestions(
        self,
        query: str,
        citations: list[Citation],
    ) -> str:
        """Generate suggested related topics."""
        suggestions = []

        # Suggest related chapters from citations
        if citations:
            unique_titles = list(set(c.title for c in citations if c.title))
            for title in unique_titles[:3]:
                suggestions.append(f"- Learn more about {title}")

        # General suggestions
        suggestions.extend([
            "- Try rephrasing your question",
            "- Ask about a specific topic covered in the book",
        ])

        return "You might want to:\n" + "\n".join(suggestions)

    def _generate_error_response(
        self,
        query: str,
        citations: list[Citation],
    ) -> ChatResponse:
        """Generate an error response."""
        return ChatResponse(
            response=(
                "I encountered an error while generating a response. "
                "Please try again or rephrase your question."
            ),
            citations=citations,
            conversation_id="",
            confidence_score=0.0,
        )

    def close(self):
        """Clean up resources."""
        self.retriever.close()
