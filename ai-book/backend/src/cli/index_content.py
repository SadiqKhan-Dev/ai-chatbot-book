"""
CLI command for indexing book content.
Usage: python -m src.cli.index_content --path ../docs
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config import get_settings
from src.services import ContentIndexer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the index-content command."""
    parser = argparse.ArgumentParser(
        description="Index book content into the vector store",
    )
    parser.add_argument(
        "--path",
        type=str,
        default="../docs",
        help="Path to directory containing markdown files",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="",
        help="Base URL prefix for chapter paths",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of chunks to process per batch",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-index even if files haven't changed",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Resolve path
    script_dir = Path(__file__).parent.parent
    content_path = Path(args.path)

    if not content_path.is_absolute():
        content_path = (script_dir / content_path).resolve()

    logger.info(f"Indexing content from: {content_path}")
    logger.info(f"Base URL: {args.base_url or '(none)'}")

    # Check directory exists
    if not content_path.exists():
        logger.error(f"Directory not found: {content_path}")
        sys.exit(1)

    if not content_path.is_dir():
        logger.error(f"Path is not a directory: {content_path}")
        sys.exit(1)

    # Initialize indexer and run
    try:
        indexer = ContentIndexer()

        status = indexer.index_directory(
            directory=content_path,
            base_url=args.base_url,
            batch_size=args.batch_size,
            force_reindex=args.force,
        )

        indexer.close()

        # Print summary
        print("\n" + "=" * 50)
        print("Indexing Complete")
        print("=" * 50)
        print(f"Files processed: {status.total_files}")
        print(f"Chunks created: {status.total_chunks}")
        print(f"Embeddings generated: {status.total_embeddings}")
        print(f"Points in collection: {status.total_points}")
        print(f"Time elapsed: {status.elapsed_seconds:.2f}s")

        if status.errors:
            print(f"\nErrors ({len(status.errors)}):")
            for error in status.errors[:5]:  # Show first 5
                print(f"  - {error}")
            if len(status.errors) > 5:
                print(f"  ... and {len(status.errors) - 5} more")

    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
