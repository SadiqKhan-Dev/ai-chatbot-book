"""
Embedding factory for creating embedding service instances.
Supports multiple providers: OpenAI, Cohere, Hugging Face.
"""

from typing import Optional

from ...core.config import get_settings
from .base import BaseEmbeddingService
from .openai_embedding import OpenAIEmbeddingService


def create_embedding_service(
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
) -> BaseEmbeddingService:
    """
    Create an embedding service for the specified provider.

    Args:
        provider: Embedding provider name ("openai", "cohere", "huggingface")
        api_key: Optional API key override

    Returns:
        BaseEmbeddingService instance for the provider

    Raises:
        ValueError: If provider is not supported
    """
    settings = get_settings()
    provider = (provider or settings.embedding_provider).lower()

    if provider == "openai":
        return OpenAIEmbeddingService(
            model_name=settings.openai_embedding_model,
            api_key=api_key or settings.openai_api_key,
        )

    elif provider == "cohere":
        from .cohere_embedding import CohereEmbeddingService

        return CohereEmbeddingService(
            model_name=settings.cohere_embedding_model,
            api_key=api_key or settings.cohere_api_key,
        )

    elif provider == "huggingface":
        from .huggingface_embedding import HuggingFaceEmbeddingService

        return HuggingFaceEmbeddingService(
            model_name=settings.hf_embedding_model,
        )

    else:
        raise ValueError(
            f"Unsupported embedding provider: {provider}. "
            f"Supported providers: openai, cohere, huggingface"
        )


class EmbeddingFactory:
    """Factory class for embedding services."""

    def __init__(self, provider: Optional[str] = None):
        """Initialize factory with optional provider override."""
        self._provider = provider

    def create(self, api_key: Optional[str] = None) -> BaseEmbeddingService:
        """Create an embedding service instance."""
        return create_embedding_service(self._provider, api_key)

    @property
    def default_provider(self) -> str:
        """Get the default embedding provider from settings."""
        settings = get_settings()
        return settings.embedding_provider

    def get_supported_providers(self) -> list[str]:
        """Get list of supported providers."""
        return ["openai", "cohere", "huggingface"]
