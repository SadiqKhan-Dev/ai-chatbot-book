"""
Indexing router for content management endpoints.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..models.indexing import IndexStatus, ReindexRequest
from ..services import ContentIndexer

router = APIRouter(prefix="/api/v1/index", tags=["indexing"])


class IndexDirectoryRequest(BaseModel):
    """Request to index a directory."""
    directory: str
    base_url: str = ""
    force_reindex: bool = False


@router.get("/status", response_model=IndexStatus)
async def get_index_status() -> IndexStatus:
    """
    Get the current indexing status.

    Returns the number of indexed chunks and collection info.
    """
    try:
        indexer = ContentIndexer()
        status = indexer.get_status()
        indexer.close()
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting index status: {str(e)}",
        )


@router.post("/reindex", response_model=IndexStatus)
async def reindex_content(request: ReindexRequest) -> IndexStatus:
    """
    Trigger a re-indexing of content.

    This will clear the existing index and re-index all content.

    - **directory**: Directory path to index
    - **base_url**: Base URL prefix for chapter paths
    - **force**: Force re-index even if files haven't changed
    """
    try:
        indexer = ContentIndexer()

        # Clear existing index
        indexer.clear_index()

        # Re-index
        status = indexer.index_directory(
            directory=Path(request.directory),
            base_url=request.base_url,
            force_reindex=request.force,
        )

        indexer.close()
        return status

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error re-indexing content: {str(e)}",
        )


@router.post("/index-directory", response_model=IndexStatus)
async def index_directory(request: IndexDirectoryRequest) -> IndexStatus:
    """
    Index a directory of markdown files.

    - **directory**: Directory path containing markdown files
    - **base_url**: Base URL prefix for chapter paths
    - **force_reindex**: Force re-index even if unchanged
    """
    try:
        indexer = ContentIndexer()

        status = indexer.index_directory(
            directory=Path(request.directory),
            base_url=request.base_url,
            force_reindex=request.force_reindex,
        )

        indexer.close()
        return status

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error indexing directory: {str(e)}",
        )


@router.delete("/clear", response_model=dict)
async def clear_index():
    """
    Clear all indexed content.
    """
    try:
        indexer = ContentIndexer()
        success = indexer.clear_index()
        indexer.close()

        if success:
            return {"status": "cleared", "message": "Index cleared successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to clear index",
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing index: {str(e)}",
        )
