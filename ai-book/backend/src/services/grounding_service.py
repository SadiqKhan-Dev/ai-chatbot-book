"""
Grounding service for response validation.
Ensures AI responses are based on book content.
"""

import logging
from typing import Optional

from ..core.config import get_settings
from ..models.chat import GroundingResult

logger = logging.getLogger(__name__)


class GroundingValidator:
    """Service for validating response grounding in source material."""

    def __init__(self, relevance_threshold: float = 0.7):
        """Initialize grounding validator."""
        settings = get_settings()
        self.threshold = settings.retrieval_relevance_threshold
        self.max_passages = settings.max_retrieved_passages

    def validate(
        self,
        query: str,
        passages: list[str],
        scores: list[float],
    ) -> GroundingResult:
        """
        Validate if a query is grounded in retrieved passages.

        Args:
            query: User's question
            passages: List of retrieved passage texts
            scores: Relevance scores for each passage

        Returns:
            GroundingResult with validation details
        """
        if not passages or not scores:
            return GroundingResult(
                is_grounded=False,
                max_relevance_score=0.0,
                passages_found=0,
            )

        max_score = max(scores) if scores else 0.0
        passages_found = len([s for s in scores if s >= self.threshold])

        return GroundingResult(
            is_grounded=max_score >= self.threshold and passages_found > 0,
            max_relevance_score=max_score,
            passages_found=passages_found,
        )

    def is_out_of_scope(
        self,
        query: str,
        max_relevance_score: float,
        min_threshold: Optional[float] = None,
    ) -> bool:
        """
        Check if a query is outside the knowledge base scope.

        Args:
            query: User's question
            max_relevance_score: Highest relevance score from retrieval
            min_threshold: Override threshold

        Returns:
            True if query is likely out of scope
        """
        threshold = min_threshold or self.threshold
        return max_relevance_score < threshold

    def get_fallback_response(
        self,
        query: str,
        related_topics: Optional[list[str]] = None,
    ) -> str:
        """
        Generate a fallback response for out-of-scope queries.

        Args:
            query: User's question
            related_topics: Optional list of related topics

        Returns:
            Fallback response text
        """
        response_parts = [
            "I don't have enough information in the book to answer this question.",
            "",
            "This question appears to be outside the scope of the current content.",
        ]

        if related_topics:
            response_parts.extend([
                "",
                "Here are some topics I can help with:",
                * [f"- {topic}" for topic in related_topics[:5]],
            ])

        response_parts.extend([
            "",
            "You might want to:",
            "- Try rephrasing your question",
            "- Ask about a specific topic covered in the book",
        ])

        return "\n".join(response_parts)

    def calculate_confidence(
        self,
        max_relevance_score: float,
        passage_count: int,
        score_variance: float = 0.1,
    ) -> float:
        """
        Calculate confidence score for a response.

        Args:
            max_relevance_score: Highest relevance score
            passage_count: Number of relevant passages
            score_variance: Variance in scores (lower = more confident)

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence on relevance
        confidence = max_relevance_score

        # Boost for multiple relevant passages
        if passage_count >= 3:
            confidence = min(confidence + 0.15, 1.0)
        elif passage_count >= 2:
            confidence = min(confidence + 0.1, 1.0)

        return confidence
