"""
Chunking service for splitting documents into manageable segments.
Implements semantic-aware text splitting for optimal RAG retrieval.
"""

import hashlib
import logging
import re
from pathlib import Path
from typing import Optional

import tiktoken

from ..models.indexing import ChunkMetadata, DocumentChunk

logger = logging.getLogger(__name__)


class MarkdownDocumentSplitter:
    """Splits markdown documents into semantic chunks."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        encoding_name: str = "cl100k_base",
    ):
        """
        Initialize the document splitter.

        Args:
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            encoding_name: TikToken encoding name for token counting
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)

    def split_markdown(
        self, content: str, source_path: str, base_url: str = ""
    ) -> list[DocumentChunk]:
        """
        Split markdown content into chunks.

        Args:
            content: Raw markdown content
            source_path: File path or URL path of the source
            base_url: Base URL for the chapter

        Returns:
            List of DocumentChunk objects
        """
        # Extract metadata from frontmatter if present
        content = self._strip_frontmatter(content)

        # Extract title from first heading
        title = self._extract_title(content, source_path)

        # Split into sections by headings
        sections = self._split_by_headings(content)

        # Further split large sections into chunks
        chunks: list[DocumentChunk] = []

        for section in sections:
            section_chunks = self._chunk_section(
                section, source_path, title, base_url
            )
            chunks.extend(section_chunks)

        logger.info(f"Split {source_path} into {len(chunks)} chunks")
        return chunks

    def _strip_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from markdown."""
        pattern = r"^---\n.*?\n---\n"
        return re.sub(pattern, "", content, flags=re.DOTALL)

    def _extract_title(self, content: str, source_path: str) -> str:
        """Extract title from first heading or use filename."""
        # Look for first H1 heading
        match = re.match(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Use filename as fallback
        return Path(source_path).stem.replace("-", " ").replace("_", " ").title()

    def _split_by_headings(self, content: str) -> list[dict]:
        """
        Split content by markdown headings.

        Returns:
            List of sections with heading level, title, and content
        """
        lines = content.split("\n")
        sections: list[dict] = []
        current_section: dict = {"level": 0, "title": "", "content": []}

        for line in lines:
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading_match:
                # Save previous section
                if current_section["content"]:
                    sections.append(current_section)

                # Start new section
                current_section = {
                    "level": len(heading_match.group(1)),
                    "title": heading_match.group(2).strip(),
                    "content": [],
                }
            else:
                current_section["content"].append(line)

        # Don't forget the last section
        if current_section["content"]:
            sections.append(current_section)

        return sections

    def _chunk_section(
        self,
        section: dict,
        source_path: str,
        chapter_title: str,
        base_url: str,
    ) -> list[DocumentChunk]:
        """Split a section into token-sized chunks."""
        # Combine section content
        text = "\n".join(section["content"]).strip()
        if not text:
            return []

        # Get tokens
        tokens = self.encoding.encode(text)
        section_title = section.get("title", "")

        if len(tokens) <= self.chunk_size:
            # Section fits in one chunk
            chunk_text = self._clean_chunk_text(text)
            return [
                DocumentChunk(
                    content=chunk_text,
                    metadata=ChunkMetadata(
                        chunk_id=self._generate_chunk_id(
                            source_path, section_title, 0
                        ),
                        source_path=source_path,
                        chapter_path=base_url or source_path,
                        title=chapter_title,
                        section_title=section_title,
                        start_token=0,
                        end_token=len(tokens),
                        char_count=len(chunk_text),
                    ),
                )
            ]

        # Split into overlapping chunks
        chunks: list[DocumentChunk] = []
        overlap_tokens = self.encoding.encode(
            " ".join(["..."] * self.chunk_overlap)
        )
        effective_chunk_size = self.chunk_size - len(overlap_tokens)

        start = 0
        chunk_index = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]

            # Decode chunk text
            chunk_text = self.encoding.decode(chunk_tokens)
            chunk_text = self._clean_chunk_text(chunk_text)

            chunks.append(
                DocumentChunk(
                    content=chunk_text,
                    metadata=ChunkMetadata(
                        chunk_id=self._generate_chunk_id(
                            source_path, section_title, chunk_index
                        ),
                        source_path=source_path,
                        chapter_path=base_url or source_path,
                        title=chapter_title,
                        section_title=section_title,
                        start_token=start,
                        end_token=end,
                        char_count=len(chunk_text),
                    ),
                )
            )

            # Move start position (accounting for overlap)
            start = end - self.chunk_overlap
            chunk_index += 1

            if start >= len(tokens):
                break

        return chunks

    def _clean_chunk_text(self, text: str) -> str:
        """Clean up chunk text for better readability."""
        # Remove excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def _generate_chunk_id(
        self, source_path: str, section_title: str, chunk_index: int
    ) -> str:
        """Generate a unique chunk ID."""
        unique_str = f"{source_path}:{section_title}:{chunk_index}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:16]

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    def close(self):
        """Close the tokenizer."""
        self.encoding.close()


class ChunkingService:
    """Service for document chunking operations."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ):
        """Initialize chunking service."""
        self.splitter = MarkdownDocumentSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def process_file(
        self, file_path: Path, base_url: str = ""
    ) -> list[DocumentChunk]:
        """Process a markdown file and return chunks."""
        content = file_path.read_text(encoding="utf-8")
        source_path = str(file_path)

        return self.splitter.split_markdown(content, source_path, base_url)

    def process_content(
        self, content: str, source_path: str, base_url: str = ""
    ) -> list[DocumentChunk]:
        """Process raw markdown content."""
        return self.splitter.split_markdown(content, source_path, base_url)

    def close(self):
        """Clean up resources."""
        self.splitter.close()
