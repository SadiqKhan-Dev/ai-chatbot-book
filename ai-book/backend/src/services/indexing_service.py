"""
Indexing service for content indexing operations.
Handles document processing, embedding generation, and Qdrant storage.
"""

import logging
from pathlib import Path
from typing import Optional

from qdrant_client.models import PointStruct

from ..core.config import get_settings
from ..models.indexing import IndexStatus
from ..services import QdrantService, create_embedding_service
from .chunking_service import ChunkingService

logger = logging.getLogger(__name__)


class ContentIndexer:
    """Service for indexing book content into the vector store."""

    def __init__(
        self,
        qdrant_service: Optional[QdrantService] = None,
        embedding_service=None,
        chunking_service: Optional[ChunkingService] = None,
    ):
        """Initialize the content indexer."""
        settings = get_settings()

        self.qdrant_service = qdrant_service or QdrantService()
        self.embedding_service = embedding_service or create_embedding_service()
        self.chunking_service = chunking_service or ChunkingService()

        logger.info(f"ContentIndexer initialized with {settings.embedding_provider} embeddings")

    def index_directory(
        self,
        directory: Path,
        base_url: str = "",
        batch_size: int = 10,
        force_reindex: bool = False,
    ) -> IndexStatus:
        """
        Index all markdown files in a directory.

        Args:
            directory: Path to directory containing markdown files
            base_url: Base URL prefix for chapter paths
            batch_size: Number of chunks to process per batch
            force_reindex: Whether to re-index already indexed content

        Returns:
            IndexStatus with indexing results
        """
        import time

        start_time = time.time()
        total_files = 0
        total_chunks = 0
        total_embeddings = 0
        errors: list[str] = []

        # Find all markdown files
        md_files = list(directory.rglob("*.md"))
        total_files = len(md_files)

        logger.info(f"Found {total_files} markdown files to index")

        # Ensure collection exists with correct vector size
        vector_size = self.embedding_service.dimension
        self.qdrant_service.ensure_collection(vector_size=vector_size)

        # Process each file
        for file_idx, md_file in enumerate(md_files, 1):
            try:
                logger.info(f"Processing [{file_idx}/{total_files}]: {md_file}")

                # Get file modification time for comparison
                file_mtime = md_file.stat().st_mtime

                # Skip if already indexed (unless force_reindex)
                if not force_reindex:
                    # TODO: Implement check for already indexed files
                    pass

                # Get chunks
                chunks = self.chunking_service.process_file(md_file, base_url)

                if not chunks:
                    logger.warning(f"No chunks generated for {md_file}")
                    continue

                # Generate embeddings
                texts = [chunk.content for chunk in chunks]
                embeddings = self.embedding_service.embed_documents(texts)

                # Create points for Qdrant
                points = []
                for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    point = PointStruct(
                        id=hash(f"{md_file}:{idx}".encode()).__hash__(),
                        vector=embedding,
                        payload={
                            "content": chunk.content,
                            "chunk_id": chunk.metadata.chunk_id,
                            "source_path": chunk.metadata.source_path,
                            "chapter_path": chunk.metadata.chapter_path,
                            "title": chunk.metadata.title,
                            "section_title": chunk.metadata.section_title or "",
                            "char_count": chunk.metadata.char_count,
                        },
                    )
                    points.append(point)

                # Upload to Qdrant
                self.qdrant_service.upsert_points(points, batch_size=batch_size)

                total_chunks += len(chunks)
                total_embeddings += len(embeddings)

                logger.info(
                    f"Indexed {len(chunks)} chunks from {md_file.name}"
                )

            except Exception as e:
                error_msg = f"Error indexing {md_file}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        elapsed_time = time.time() - start_time

        # Get final count
        total_points = self.qdrant_service.count_points()

        return IndexStatus(
            total_files=total_files,
            total_chunks=total_chunks,
            total_embeddings=total_embeddings,
            total_points=total_points,
            elapsed_seconds=elapsed_time,
            errors=errors,
        )

    def index_content(
        self,
        content: str,
        source_path: str,
        chapter_path: str = "",
        batch_size: int = 10,
    ) -> int:
        """
        Index raw content directly.

        Args:
            content: Raw markdown content
            source_path: Source file path or identifier
            chapter_path: URL path for the chapter
            batch_size: Batch size for embedding generation

        Returns:
            Number of chunks indexed
        """
        # Get chunks
        chunks = self.chunking_service.process_content(
            content, source_path, chapter_path or source_path
        )

        if not chunks:
            return 0

        # Generate embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_service.embed_documents(texts)

        # Create points
        points = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=hash(f"{source_path}:{idx}".encode()).__hash__(),
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "chunk_id": chunk.metadata.chunk_id,
                    "source_path": chunk.metadata.source_path,
                    "chapter_path": chunk.metadata.chapter_path,
                    "title": chunk.metadata.title,
                    "section_title": chunk.metadata.section_title or "",
                    "char_count": chunk.metadata.char_count,
                },
            )
            points.append(point)

        # Upload
        self.qdrant_service.upsert_points(points, batch_size=batch_size)

        return len(chunks)

    def clear_index(self) -> bool:
        """Clear all content from the index."""
        return self.qdrant_service.delete_collection()

    def get_status(self) -> IndexStatus:
        """Get current indexing status."""
        total_points = self.qdrant_service.count_points()

        return IndexStatus(
            total_files=0,
            total_chunks=0,
            total_embeddings=0,
            total_points=total_points,
            elapsed_seconds=0,
            errors=[],
        )

    def close(self):
        """Clean up resources."""
        self.chunking_service.close()
        self.qdrant_service.close()
