"""
Selected context service for handling user-selected text in chat interactions.
Provides context building for when users select specific text passages.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field


class SelectedContext(BaseModel):
    """Represents selected text context from the user."""
    text: str = Field(..., description="The selected text content")
    start_position: int = Field(0, ge=0, description="Character start position")
    end_position: int = Field(0, ge=0, description="Character end position")
    source_reference: Optional[str] = Field(None, description="Source document/chapter")


class ContextResult(BaseModel):
    """Result of building context from selected text."""
    enriched_prompt: str = Field(..., description="Prompt with selected context integrated")
    context_length: int = Field(..., description="Length of context added")
    was_truncated: bool = Field(False, description="Whether context was truncated")


class ContextBuilder:
    """
    Builds context from user-selected text for enhanced chat responses.

    Handles:
    - Validation of selected text length
    - Context integration into prompts
    - Truncation for very long selections
    """

    MAX_SELECTION_LENGTH = 1000
    CONTEXT_PREFIX = "\n[Selected Context]:\n"
    CONTEXT_SUFFIX = "\n[/Selected Context]\n"

    def __init__(
        self,
        max_length: int = MAX_SELECTION_LENGTH,
        context_prefix: str = CONTEXT_PREFIX,
        context_suffix: str = CONTEXT_SUFFIX,
    ):
        """
        Initialize ContextBuilder.

        Args:
            max_length: Maximum allowed selection length
            context_prefix: Prefix for context integration
            context_suffix: Suffix for context integration
        """
        self._max_length = max_length
        self._context_prefix = context_prefix
        self._context_suffix = context_suffix

    def validate_selection(self, selected_text: str) -> tuple[bool, str]:
        """
        Validate the selected text.

        Args:
            selected_text: The text selected by the user

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not selected_text or not selected_text.strip():
            return False, "Selected text cannot be empty"

        if len(selected_text) > self._max_length:
            return False, f"Selected text exceeds maximum length of {self._max_length} characters"

        # Check for meaningful content (not just whitespace)
        if not re.search(r'\S', selected_text):
            return False, "Selected text contains no meaningful content"

        return True, ""

    def build_context(self, selected_text: str, original_query: str) -> ContextResult:
        """
        Build enriched context from selected text.

        Args:
            selected_text: The text selected by the user
            original_query: The user's original question

        Returns:
            ContextResult with enriched prompt
        """
        # Validate selection
        is_valid, error = self.validate_selection(selected_text)
        if not is_valid:
            raise ValueError(error)

        # Clean and truncate if needed
        cleaned_text = selected_text.strip()

        # Check if truncation is needed
        needs_truncation = len(cleaned_text) > self._max_length
        if needs_truncation:
            cleaned_text = cleaned_text[: self._max_length]

        # Build the enriched prompt
        context_content = f"User's selected text:\n{cleaned_text}"
        enriched_prompt = (
            f"{self._context_prefix}"
            f"{context_content}"
            f"{self._context_suffix}"
            f"\nBased on the selected text above, please answer: {original_query}"
        )

        return ContextResult(
            enriched_prompt=enriched_prompt,
            context_length=len(context_content),
            was_truncated=needs_truncation,
        )

    def create_followup_prompt(
        self,
        selected_text: str,
        query: str,
        system_prompt: str,
    ) -> str:
        """
        Create a complete prompt with selected context.

        Args:
            selected_text: The text selected by the user
            query: The user's question
            system_prompt: Base system prompt

        Returns:
            Complete prompt ready for LLM
        """
        context_result = self.build_context(selected_text, query)
        return f"{system_prompt}\n\n{context_result.enriched_prompt}"

    def extract_keywords(self, text: str) -> list[str]:
        """
        Extract potential keywords from selected text for retrieval enhancement.

        Args:
            text: The selected text

        Returns:
            List of extracted keywords
        """
        # Simple keyword extraction - split on non-alphanumeric
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Filter common stopwords
        stopwords = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'had', 'her', 'was', 'one', 'our', 'out', 'has',
            'have', 'been', 'this', 'that', 'with', 'they', 'from',
        }

        keywords = [w for w in words if w not in stopwords]

        # Return top 10 most frequent
        from collections import Counter
        return [kw for kw, _ in Counter(keywords).most_common(10)]


# Convenience function
def build_selected_context(selected_text: str, query: str) -> ContextResult:
    """
    Build context from selected text.

    Args:
        selected_text: The text selected by the user
        query: The user's original question

    Returns:
        ContextResult with enriched prompt
    """
    builder = ContextBuilder()
    return builder.build_context(selected_text, query)
