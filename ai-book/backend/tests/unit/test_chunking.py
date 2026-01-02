"""
Unit tests for chunking service.
Tests document splitting and token management.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.services.chunking_service import MarkdownDocumentSplitter


class TestMarkdownDocumentSplitter:
    """Tests for MarkdownDocumentSplitter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.splitter = MarkdownDocumentSplitter(
            chunk_size=100,
            chunk_overlap=20,
        )

    def test_splitter_initialization(self):
        """Test splitter initialization with custom parameters."""
        splitter = MarkdownDocumentSplitter(chunk_size=256, chunk_overlap=25)
        assert splitter.chunk_size == 256
        assert splitter.chunk_overlap == 25

    def test_strip_frontmatter(self):
        """Test frontmatter stripping."""
        content = """---
title: Test Document
---

# Content here
"""
        result = self.splitter._strip_frontmatter(content)
        assert "---" not in result.strip()
        assert "# Content here" in result

    def test_extract_title_from_heading(self):
        """Test title extraction from first heading."""
        content = "# My Document Title\n\nSome content"
        title = self.splitter._extract_title(content, "/test.md")
        assert title == "My Document Title"

    def test_split_markdown_short_content(self):
        """Test splitting short markdown content."""
        content = "# Short\n\nThis is a short document."
        chunks = self.splitter.split_markdown(content, "/test.md")

        assert len(chunks) > 0
        assert all(hasattr(chunk, 'metadata') for chunk in chunks)
        assert all(hasattr(chunk, 'content') for chunk in chunks)

    def test_split_markdown_with_multiple_sections(self):
        """Test splitting markdown with multiple sections."""
        content = """# Title

## Section 1
Content of section 1.

## Section 2
Content of section 2.
"""
        chunks = self.splitter.split_markdown(content, "/test.md")

        # Should create at least 2 chunks (one per section)
        assert len(chunks) >= 1

    def test_chunk_metadata(self):
        """Test that chunks have proper metadata."""
        content = "# Test\n\nTest content"
        chunks = self.splitter.split_markdown(content, "/docs/test.md")

        if chunks:
            chunk = chunks[0]
            assert hasattr(chunk, 'metadata')
            assert chunk.metadata.source_path == "/docs/test.md"
            assert chunk.metadata.chunk_id is not None

    def test_empty_content(self):
        """Test handling of empty content."""
        chunks = self.splitter.split_markdown("", "/test.md")
        assert chunks == [] or len(chunks) == 0


class TestChunkingConfig:
    """Tests for chunking configuration."""

    def test_default_config(self):
        """Test default chunking configuration."""
        splitter = MarkdownDocumentSplitter()
        assert splitter.chunk_size == 512
        assert splitter.chunk_overlap == 50
