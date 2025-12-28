"""
Main CLI entry point for the AI Assistant RAG.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Main CLI entry point."""
    print("AI Assistant RAG CLI")
    print("Available commands:")
    print("  index-content - Index book content into the vector store")
    print("  serve         - Start the FastAPI server")
    print()
    print("Use 'python -m src.cli.index_content --help' for indexing options")
    print("Use 'uvicorn src.main:app --reload' to start the server")


if __name__ == "__main__":
    main()
