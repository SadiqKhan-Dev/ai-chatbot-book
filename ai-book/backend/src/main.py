"""
AI Assistant RAG Backend
FastAPI application for the Physical AI & Robotics book assistant.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import chat_router, health_router, search_router, indexing_router, conversation_router
from .core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    settings = get_settings()
    logger.info(f"Starting AI Assistant RAG Backend (debug={settings.debug})")
    logger.info(f"Embedding provider: {settings.embedding_provider}")
    logger.info(f"Qdrant URL: {settings.qdrant_url}")
    yield
    logger.info("Shutting down AI Assistant RAG Backend")


# Create FastAPI application
app = FastAPI(
    title="AI Assistant RAG API",
    description="RAG-powered AI Assistant for the Physical AI & Robotics book",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router.router)
app.include_router(chat_router.router)
app.include_router(search_router.router)
app.include_router(indexing_router.router)
app.include_router(conversation_router.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AI Assistant RAG Backend",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


def create_app() -> FastAPI:
    """Factory function for creating the FastAPI app."""
    return app
