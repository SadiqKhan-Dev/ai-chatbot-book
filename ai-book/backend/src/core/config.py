"""
Core configuration for AI Assistant RAG Backend.
Loads environment variables with Pydantic validation.
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App Configuration
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    debug: bool = Field(default=False)

    # Embedding Provider
    embedding_provider: str = Field(
        default="openai",
        description="Embedding provider: openai, cohere, huggingface",
    )

    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None)
    openai_embedding_model: str = Field(default="text-embedding-3-small")
    openai_chat_model: str = Field(default="gpt-4o-mini")

    # Cohere Configuration
    cohere_api_key: Optional[str] = Field(default=None)
    cohere_embedding_model: str = Field(default="embed-english-v3.0")

    # Hugging Face Configuration
    hf_embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Qdrant Configuration
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: Optional[str] = Field(default=None)
    qdrant_collection_name: str = Field(default="book_chunks")

    # RAG Configuration
    retrieval_relevance_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0
    )
    max_retrieved_passages: int = Field(default=5, ge=1, le=20)
    max_context_tokens: int = Field(default=4000, ge=1000, le=16000)
    chat_history_messages: int = Field(default=5, ge=0, le=20)

    # Book Content Path
    book_content_path: str = Field(default="../docs")

    # Session Storage
    session_storage: str = Field(default="file", pattern="^(file|redis)$")
    redis_url: Optional[str] = Field(default=None)
    sessions_dir: str = Field(default="./sessions")

    @field_validator("embedding_provider")
    @classmethod
    def validate_embedding_provider(cls, v: str) -> str:
        valid_providers = ["openai", "cohere", "huggingface"]
        if v.lower() not in valid_providers:
            raise ValueError(
                f"Invalid embedding provider: {v}. "
                f"Must be one of: {valid_providers}"
            )
        return v.lower()

    @property
    def embedding_model(self) -> str:
        """Get the appropriate embedding model based on provider."""
        if self.embedding_provider == "openai":
            return self.openai_embedding_model
        elif self.embedding_provider == "cohere":
            return self.cohere_embedding_model
        else:
            return self.hf_embedding_model

    @property
    def embedding_api_key(self) -> Optional[str]:
        """Get the API key for the current embedding provider."""
        if self.embedding_provider == "openai":
            return self.openai_api_key
        elif self.embedding_provider == "cohere":
            return self.cohere_api_key
        return None

    def get_book_content_path(self) -> Path:
        """Get the absolute path to book content directory."""
        # Resolve relative to this file's parent (backend/)
        backend_dir = Path(__file__).parent.parent
        content_path = Path(self.book_content_path)

        if content_path.is_absolute():
            return content_path
        return (backend_dir / content_path).resolve()

    def get_sessions_dir(self) -> Path:
        """Get the absolute path to sessions directory."""
        backend_dir = Path(__file__).parent.parent
        sessions_path = Path(self.sessions_dir)

        if sessions_path.is_absolute():
            return sessions_path
        return (backend_dir / sessions_path).resolve()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience function for accessing settings
settings = get_settings()
