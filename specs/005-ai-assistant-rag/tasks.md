# Implementation Tasks: AI Assistant RAG System

**Feature**: AI Assistant RAG System
**Branch**: `005-ai-assistant-rag`
**Created**: 2025-12-28
**Priority Order**: US1 (P1) → US2 (P1) → US6 (P1) → US3 (P2) → US4 (P2) → US5 (P2)

## MVP Scope

**Minimum Viable Product**: User Story 1 (Book Content Q&A) with foundational setup
- Complete Phase 1 (Setup) and Phase 2 (Foundational)
- Complete Phase 3 (US1): Basic Q&A with OpenAI embeddings
- Can be tested independently by asking a question and receiving a response

---

## Phase 1: Project Setup

**Goal**: Initialize backend project structure and dependencies

**Independent Test Criteria**: Backend server starts without errors and serves health endpoint

### Tasks

- [X] T001 Create Python virtual environment and pyproject.toml in ai-book/backend/
- [X] T002 [P] Add FastAPI, uvicorn, pydantic, python-dotenv to dependencies
- [X] T003 [P] Add LangChain, langchain-qdrant, langchain-openai to dependencies
- [X] T004 [P] Add Cohere SDK and sentence-transformers (Hugging Face) to dependencies
- [X] T005 Create src/api/ directory structure with __init__.py files
- [X] T006 Create src/services/ directory structure with __init__.py files
- [X] T007 Create src/models/ directory structure with __init__.py files
- [X] T008 Create src/core/ directory structure with __init__.py files
- [X] T009 Create src/cli/ directory structure with __init__.py files
- [X] T010 Create tests/unit/ directory structure with __init__.py files
- [X] T011 Create tests/integration/ directory structure with __init__.py files
- [X] T012 Create .env.example with OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY placeholders
- [X] T013 Create docker-compose.yml for local Qdrant development

---

## Phase 2: Foundational Components

**Goal**: Create core configuration, models, and infrastructure used by all user stories

**Independent Test Criteria**: All models validate correctly, Qdrant connection established, embeddings generated successfully

### Tasks

- [X] T020 Create src/core/config.py with Pydantic BaseSettings for environment loading
- [X] T021 Create src/core/__init__.py exporting config and initialize functions
- [X] T022 Create src/models/chat.py with ChatRequest, ChatResponse, Citation Pydantic models
- [X] T023 Create src/models/conversation.py with Conversation, Message Pydantic models
- [X] T024 Create src/models/indexing.py with IndexStatus, ReindexRequest, ChunkMetadata models
- [X] T025 Create src/models/__init__.py exporting all models
- [X] T026 Create src/services/qdrant_client.py with Qdrant connection and collection management
- [X] T027 Create src/services/embedding_service.py with OpenAIEmbeddingService class
- [X] T028 Create src/services/embedding_factory.py with EmbeddingFactory for multi-provider support
- [X] T029 Create src/services/__init__.py exporting all services

---

## Phase 3: User Story 1 - Book Content Q&A

**Goal**: Implement core Q&A functionality with RAG pipeline (OpenAI embeddings + Qdrant retrieval)

**Independent Test Criteria**: User can ask a question about book content and receive answer with citations from indexed content

**Priority**: P1 (Core value proposition)

### Tasks

- [X] T040 Create src/services/chunking_service.py with MarkdownDocumentSplitter class
- [X] T041 [US1] Implement content chunking logic with 512-token chunks and 50-token overlap
- [X] T042 [US1] Create src/services/indexing_service.py with ContentIndexer class
- [X] T043 [US1] Implement index_content CLI command in src/cli/index_content.py
- [X] T044 [US1] Create src/services/retrieval_service.py with SemanticRetriever class
- [X] T045 [US1] Implement similarity search with relevance threshold (default 0.7)
- [X] T046 [US1] Create src/services/generation_service.py with ResponseGenerator class
- [X] T047 [US1] Implement RAG pipeline: retrieve passages → build context → generate response
- [X] T048 [US1] Create src/api/chat_router.py with POST /api/v1/chat endpoint
- [X] T049 [US1] Implement chat endpoint to accept query, run RAG pipeline, return response
- [X] T050 [US1] Create src/main.py with FastAPI app initialization and CORS configuration
- [X] T051 [US1] Add health endpoint GET /api/v1/health in src/api/health_router.py

---

## Phase 4: User Story 2 - Context-Aware Responses

**Goal**: Implement source citation system with clickable references

**Independent Test Criteria**: Every AI response includes citations with chapter titles and paths

**Priority**: P1 (Essential for educational trust)

### Tasks

- [X] T060 [US2] Update Citation model in src/models/chat.py to include chapter_path and title
- [X] T061 [US2] Modify retrieval_service.py to return passages with full metadata
- [X] T062 [US2] Update generation_service.py to format citations in response with links
- [X] T063 [US2] Create src/api/search_router.py with GET /api/v1/search endpoint
- [X] T064 [US2] Implement semantic search returning results with excerpts

---

## Phase 5: User Story 6 - Response Grounding

**Goal**: Ensure AI only answers based on book content with proper fallback messaging

**Independent Test Criteria**: Questions outside book scope receive appropriate "I don't know" response

**Priority**: P1 (Critical for educational integrity)

### Tasks

- [X] T070 [US6] Create src/services/grounding_service.py with GroundingValidator class
- [X] T071 [US6] Implement out-of-scope detection with relevance threshold check
- [X] T072 [US6] Add fallback response template for unanswerable questions
- [X] T073 [US6] Implement suggestion system to recommend related topics
- [X] T074 [US6] Add confidence scoring to generation_service.py responses

---

## Phase 6: User Story 3 - Selected Text Q&A

**Goal**: Allow users to select text and ask contextual questions

**Independent Test Criteria**: Selected text is passed as context and responses address the specific content

**Priority**: P2 (Enhanced reading experience)

### Tasks

- [X] T080 [US3] Update ChatRequest model in src/models/chat.py to include selected_text field
- [X] T081 [US3] Modify retrieval_service.py to prioritize selected text context when provided
- [X] T082 [US3] Update generation_service.py to incorporate selected text in prompt
- [X] T083 [US3] Create src/services/selected_context_service.py with ContextBuilder class
- [X] T084 [US3] Implement selected text validation (max 1000 characters)

---

## Phase 7: User Story 4 - Conversation History

**Goal**: Persist conversation history within and across sessions

**Independent Test Criteria**: Users see previous questions and can continue conversations

**Priority**: P2 (Learning continuity)

### Tasks

- [X] T090 [US4] Create src/services/conversation_service.py with ConversationManager class
- [X] T091 [US4] Implement session storage using local filesystem or Redis
- [X] T092 [US4] Create src/api/conversation_router.py with GET /api/v1/chat/{conversation_id} endpoint
- [X] T093 [US4] Add GET /api/v1/chat/{conversation_id}/messages endpoint
- [X] T094 [US4] Implement conversation ID generation and tracking in chat endpoint
- [X] T095 [US4] Add conversation title generation from first query

---

## Phase 8: User Story 5 - Topic-Specific Knowledge (Cohere/Hugging Face)

**Goal**: Support alternative embedding providers for uv, FastAPI, Qdrant, Cohere, Hugging Face topics

**Independent Test Criteria**: Cohere and Hugging Face embeddings work correctly and can be selected

**Priority**: P2 (Specific requirement)

### Tasks

- [X] T100 [US5] Create src/services/embeddings/cohere_embedding.py with CohereEmbeddingService
- [X] T101 [US5] Create src/services/embeddings/huggingface_embedding.py with HuggingFaceEmbeddingService
- [X] T102 [US5] Implement embedding provider configuration in embedding_factory.py
- [X] T103 [US5] Add provider selection via environment variable (EMBEDDING_PROVIDER)
- [X] T104 [US5] Create src/services/embeddings/__init__.py exporting all embedding services
- [X] T105 [US5] Implement batch embedding for indexing with progress tracking
- [X] T106 [US5] Add embedding caching to avoid redundant API calls

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Final refinements, testing, and deployment configuration

**Independent Test Criteria**: All tests pass, API docs available, deployment succeeds

### Tasks

- [X] T110 Create pytest.ini and configure test discovery
- [X] T111 Write unit tests for chunking_service.py in tests/unit/test_chunking.py
- [X] T112 Write unit tests for retrieval_service.py in tests/unit/test_retrieval.py
- [X] T113 Write unit tests for models in tests/unit/test_models.py
- [X] T114 Write integration tests for chat endpoint in tests/integration/test_chat_api.py
- [X] T115 Create tests/contract/ directory with OpenAPI spec validation tests
- [X] T116 Add error handling middleware in src/api/middleware.py
- [X] T117 Implement request logging and correlation IDs
- [X] T118 Create Dockerfile for backend containerization
- [X] T119 Add Render.yaml or fly.toml for platform deployment
- [X] T120 Create .env.production with production configuration templates

---

## Task Summary

| Phase | User Story | Task Count | Description |
|-------|------------|------------|-------------|
| 1 | Setup | 13 | Project initialization |
| 2 | Foundational | 10 | Core infrastructure |
| 3 | US1 | 12 | Core Q&A with RAG |
| 4 | US2 | 5 | Source citations |
| 5 | US6 | 5 | Response grounding |
| 6 | US3 | 5 | Selected text mode |
| 7 | US4 | 6 | Conversation history |
| 8 | US5 | 7 | Cohere/Hugging Face |
| 9 | Polish | 11 | Testing, deployment |
| **Total** | | **74** | |

---

## Dependency Graph

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational: models, embedding, qdrant)
    │
    ▼
┌───────────────────────────────────────────────────────┐
│ Phase 3 (US1): Core RAG pipeline                      │
│   - Depends on: embeddings, qdrant, models            │
│   - Blocks: US2, US3, US4, US5, US6                   │
└───────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────┬──────────────────┬──────────────────┐
│ Phase 4 (US2)    │ Phase 5 (US6)    │ Phase 6 (US3)    │
│ Source citations │ Response grounding│ Selected text   │
│ (can parallelize │ (can parallelize │ (can parallelize │
│  with US3, US4)  │  with US2, US3)  │  with US2, US4)  │
└──────────────────┴──────────────────┴──────────────────┘
    │         │                  │
    └─────────┼──────────────────┘
              ▼
┌───────────────────────────────────────────────────────┐
│ Phase 7 (US4): Conversation History                   │
│   - Depends on: US1                                   │
└───────────────────────────────────────────────────────┘
              │
              ▼
┌───────────────────────────────────────────────────────┐
│ Phase 8 (US5): Cohere/Hugging Face Support            │
│   - Depends on: US1, US3 (for embedding integration)  │
└───────────────────────────────────────────────────────┘
              │
              ▼
┌───────────────────────────────────────────────────────┐
│ Phase 9 (Polish): Testing, deployment                 │
│   - Depends on: All previous phases complete          │
└───────────────────────────────────────────────────────┘
```

---

## Parallel Execution Opportunities

### Within User Stories (US1 parallelizable tasks):
- T040, T041: Chunking service development
- T042, T043: Indexing service and CLI
- T044, T045: Retrieval service implementation
- T048, T049: API endpoints

### Between User Stories (US2, US3, US4 can run in parallel):
- US2 (Citations): T060-T064
- US3 (Selected Text): T080-T084
- US4 (History): T090-T095

All three can be implemented concurrently after Phase 3 (US1) is complete.

---

## Independent Testing Instructions

### Test Phase 1 (Setup):
```bash
cd ai-book/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# Verify http://localhost:8000/api/v1/health returns 200
```

### Test Phase 2 (Foundational):
```bash
# Test models
pytest tests/unit/test_models.py -v

# Test embeddings
python -c "from services.embedding_service import OpenAIEmbeddingService; e = OpenAIEmbeddingService(); print(e.embed('test'))"
```

### Test Phase 3 (US1 - Core Q&A):
```bash
# Index book content
python -m cli.index_content --path ../docs --batch-size 10

# Test chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a digital twin?"}'
# Verify response includes answer and citations
```

### Test Phase 4 (US2 - Citations):
```bash
# Verify citations in response
curl http://localhost:8000/api/v1/search?q=digital twin
# Verify results include chapter_path and title
```

---

## Implementation Strategy

### MVP First (Phase 1-3):
1. Complete setup and foundational components
2. Implement US1 with OpenAI embeddings only
3. Test basic Q&A functionality
4. Deploy to Render/Fly.io for validation

### Incremental Delivery:
1. After MVP: Add US2 (citations) and US6 (grounding)
2. Then: Add US3 (selected text) and US4 (history)
3. Finally: Add US5 (Cohere/Hugging Face support)

### Each User Story is independently testable:
- US1: Ask question → get answer (basic test)
- US2: Ask question → get answer with citations (enhanced test)
- US3: Select text → ask question → response addresses selection
- US4: Ask questions → refresh → history visible
- US5: Switch embedding provider → same Q&A works
- US6: Ask out-of-scope question → appropriate fallback
