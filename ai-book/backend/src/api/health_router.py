"""
Health check router for API status monitoring.
"""

from fastapi import APIRouter

from ..models.indexing import HealthStatus
from ..services import QdrantService, create_embedding_service

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """
    Check the health status of the API and its dependencies.

    Returns:
        HealthStatus with component statuses
    """
    components = {}
    overall_status = "healthy"

    # Check Qdrant connection
    try:
        qdrant_service = QdrantService()
        point_count = qdrant_service.count_points()
        qdrant_service.close()

        components["qdrant"] = {
            "status": "healthy",
            "points_count": point_count,
        }
    except Exception as e:
        components["qdrant"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        overall_status = "degraded"

    # Check embedding service
    try:
        embedding_service = create_embedding_service()
        _ = embedding_service.dimension  # Test access

        components["embeddings"] = {
            "status": "healthy",
            "provider": embedding_service.model_name,
        }
    except Exception as e:
        components["embeddings"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        overall_status = "degraded"

    return HealthStatus(
        status=overall_status,
        components=components,
        version="0.1.0",
    )


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe endpoint."""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe endpoint."""
    return {"status": "alive"}
