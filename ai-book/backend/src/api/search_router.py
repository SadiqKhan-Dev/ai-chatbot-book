"""
Search router for semantic search endpoint.
"""

from fastapi import APIRouter

from ..models.indexing import SearchQuery, SearchResult
from ..services import SemanticRetriever

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("", response_model=list[SearchResult])
async def search_endpoint(
    q: str,
    limit: int = 5,
    threshold: float = 0.7,
) -> list[SearchResult]:
    """
    Search the book content semantically.

    Returns passages from the indexed content that match the query.

    - **q**: Search query
    - **limit**: Maximum number of results (default: 5)
    - **threshold**: Minimum relevance score (default: 0.7)
    """
    retriever = SemanticRetriever()

    results = retriever.search(
        query=q,
        limit=limit,
        threshold=threshold,
    )

    retriever.close()
    return results


@router.post("", response_model=list[SearchResult])
async def search_post(
    query: SearchQuery,
) -> list[SearchResult]:
    """
    Search the book content semantically (POST method).

    Returns passages from the indexed content that match the query.
    """
    retriever = SemanticRetriever()

    results = retriever.search(
        query=query.query,
        selected_text=query.selected_text,
        context_chapter=query.context_chapter,
        limit=query.limit,
        threshold=query.threshold,
    )

    retriever.close()
    return results
