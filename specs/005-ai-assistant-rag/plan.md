# Implementation Plan: AI Assistant RAG System

**Branch**: `005-ai-assistant-rag` | **Date**: 2025-12-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-ai-assistant-rag/spec.md`

## Summary

Build a RAG-powered AI assistant for the Physical AI & Robotics Docusaurus book that answers user questions about book content. The system indexes book content into Qdrant vector database, provides a FastAPI backend with OpenAI Agents SDK for intelligent responses, and embeds a chat UI into the Docusaurus site. Supports queries on uv, FastAPI, Qdrant, Cohere, and Hugging Face topics with strict source grounding.

## Technical Context

**Language/Version**: Python 3.11+ (FastAPI backend), TypeScript/React (Docusaurus UI)
**Primary Dependencies**: FastAPI, Qdrant, OpenAI Agents SDK or LangChain, Docusaurus React
**Storage**: Qdrant (vector embeddings), local filesystem (book content), optional Redis (sessions)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Linux server (backend), web browser (Docusaurus frontend)
**Performance Goals**: <10s response time for 90% of queries, support 200 concurrent users
**Constraints**: Must use OpenAI Agents SDK or ChatKit SDK for RAG; must embed in existing Docusaurus
**Scale/Scope**: Single-book knowledge base (~100-500 pages of content)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution template is empty (no specific rules defined). Standard software engineering practices apply:
- Write tests before implementation
- Maintain clean code structure
- Document all APIs and components
- Use version control for all changes

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-assistant-rag/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
ai-book/
├── backend/                    # FastAPI RAG backend
│   ├── src/
│   │   ├── api/               # FastAPI routes and endpoints
│   │   ├── services/          # Business logic (indexing, retrieval, generation)
│   │   ├── models/            # Pydantic models, data structures
│   │   ├── core/              # Configuration, initialization
│   │   └── cli/               # CLI tools for indexing, management
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── contract/
│   ├── requirements.txt
│   └── pyproject.toml
│
├── ai-assistant/              # Docusaurus swizzled component
│   ├── src/
│   │   └── theme/
│   │       └── AIAssistant/   # React chat interface
│   └── package.json
│
├── scripts/
│   ├── index-content.py       # Script to index book content
│   └── deploy.sh              # Deployment automation
│
└── docker-compose.yml         # Local development services
```

**Structure Decision**: Backend in `ai-book/backend/` with FastAPI, frontend component in `ai-book/src/theme/AIAssistant/` for Docusaurus integration, shared scripts for indexing and deployment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Two project types (backend + Docusaurus swizzle) | FastAPI needed for RAG processing; UI must embed in Docusaurus | Single-page app would require rebuilding Docusaurus from scratch |
| Multiple services (Qdrant + FastAPI) | Vector search requires dedicated vector DB | In-memory vectors insufficient for production scale |
| Separate embedding service | OpenAI API rate limits, cost optimization | Direct API calls work but less efficient |

---

# Phase 0: Research & Unknowns

## Unknowns to Resolve

| # | Unknown | Research Task |
|---|---------|---------------|
| U1 | OpenAI Agents SDK vs ChatKit SDK for RAG | Research both SDKs for RAG implementation patterns |
| U2 | Qdrant indexing strategy for Docusaurus | Research best practices for chunking Markdown content |
| U3 | Docusaurus React component embedding | Research swizzling patterns for custom components |
| U4 | Deployment options for backend on budget | Research Render, Railway, Fly.io, or similar PaaS |
| U5 | OpenAI embedding model selection | Research text-embedding-3-small vs large |

## Research Findings

### U1: OpenAI Agents SDK vs ChatKit SDK for RAG

**Decision**: Use OpenAI Agents SDK with LangChain integration

**Rationale**:
- OpenAI Agents SDK provides native tool calling and context management
- LangChain offers proven RAG abstractions ( retrievers, document loaders)
- ChatKit is primarily for chat UIs, not backend RAG logic

**Implementation approach**:
- Use `langchain-qdrant` for vector retrieval
- Use `langchain-openai` for chat completions
- Build custom agent with retrieval tool

### U2: Qdrant Indexing Strategy

**Decision**: Semantic chunking with overlap

**Rationale**:
- Docusaurus Markdown files map naturally to document chunks
- Semantic chunking preserves code blocks and related explanations together
- 512-token chunks with 50-token overlap balance relevance and context

**Implementation approach**:
- Parse Markdown with frontmatter for metadata
- Split on headers while keeping code blocks intact
- Store chapter/section path as payload for citation generation

### U3: Docusaurus React Component Embedding

**Decision**: Swizzle Layout component to add chat widget

**Rationale**:
- Docusaurus supports component swizzling for theme customization
- Layout swizzle allows persistent chat across all pages
- Chat widget positioned as floating FAB or sidebar

**Implementation approach**:
- Swizzle `@theme/Layout` to include ChatWidget
- ChatWidget uses React context for state management
- Communication via fetch/axios to FastAPI backend

### U4: Backend Deployment Options

**Decision**: Deploy to Render or Fly.io with Qdrant Cloud

**Rationale**:
- Qdrant Cloud offers free tier sufficient for development
- Render/Fly.io provide affordable Python hosting ($5-25/mo)
- GitHub Actions for CI/CD deployment automation

**Implementation approach**:
- Backend: Render web service or Fly.io app
- Vector DB: Qdrant Cloud free tier
- Environment: Docker container or pip install

### U5: Embedding Model Selection

**Decision**: text-embedding-3-small

**Rationale**:
- 60% cheaper than text-embedding-3-large
- Sufficient quality for RAG (1536 dimensions)
- Good balance of cost and performance

**Implementation approach**:
- Use OpenAI `text-embedding-3-small` model
- Batch embeddings during indexing for efficiency
- Cache embeddings for re-indexing scenarios

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docusaurus Site                           │
│  (GitHub Pages)                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    AI Assistant Widget                       ││
│  │  ┌─────────────┐    ┌─────────────────────────────────────┐ ││
│  │  │ Chat Window │←──→│ FastAPI Backend (Render/Fly.io)     │ ││
│  │  └─────────────┘    │  ┌─────────────────────────────────┐│ ││
│  │                      │  │ RAG Agent (OpenAI Agents SDK)   ││ ││
│  │                      │  └─────────────────────────────────┘│ ││
│  │                      │  ┌─────────────────────────────────┐│ ││
│  │                      │  │ Embeddings (OpenAI)             ││ ││
│  │                      │  └─────────────────────────────────┘│ ││
│  │                      └─────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
                    ┌─────────────────────┐
                    │   Qdrant Cloud      │
                    │   (Vector Database) │
                    └─────────────────────┘
```

---

# Phase 1: Design & Contracts

## Data Model

### Key Entities

| Entity | Fields | Description |
|--------|--------|-------------|
| **DocumentChunk** | id, content, metadata, embedding, chapter_path | Individual chunk of indexed book content |
| **Conversation** | id, user_id, created_at, title | User conversation session |
| **Message** | id, conversation_id, role, content, timestamp, citations | Individual chat message with sources |
| **UserQuery** | id, query_text, selected_text, context_chapter, timestamp | User's question with optional text selection |

### Relationships

```
Conversation (1) ───┐ (N) Message
                    │
UserQuery (N) ───┐  │
                 │  └── (N) Citation (link to DocumentChunk)
                 │
                 └── (N) DocumentChunk (retrieved passages)
```

## API Contracts

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send a question and get AI response |
| GET | `/api/v1/chat/{conversation_id}` | Get conversation history |
| GET | `/api/v1/chat/{conversation_id}/messages` | Get messages in conversation |
| POST | `/api/v1/index` | Trigger content re-indexing (admin) |
| GET | `/api/v1/health` | Health check endpoint |

### Request/Response Schemas

**POST /api/v1/chat**

Request:
```json
{
  "query": "What is a digital twin?",
  "selected_text": null,
  "conversation_id": null,
  "context_chapter": "/docs/digital-twin"
}
```

Response:
```json
{
  "response": "A digital twin is a virtual representation...",
  "citations": [
    {
      "chunk_id": "abc123",
      "chapter_path": "/docs/physical-ai-robotics-course",
      "title": "Module 2: Digital Twin (Gazebo & Unity)",
      "relevance_score": 0.92
    }
  ],
  "conversation_id": "conv_xyz789"
}
```

### WebSocket (optional for streaming)

```json
{
  "type": "message",
  "query": "Explain FastAPI routing",
  "stream": true
}
```

---

# Phase 2: Implementation Tasks

*To be generated by `/sp.tasks` command*

1. Backend setup (FastAPI project, dependencies)
2. Content indexing pipeline (Markdown parsing, embedding, Qdrant)
3. RAG agent implementation (OpenAI Agents SDK, retrieval tool)
4. API endpoints (chat, history, health)
5. Docusaurus swizzle (Layout component, ChatWidget)
6. React chat UI (message list, input, loading states)
7. Backend deployment (Docker, Render/Fly.io config)
8. CI/CD pipeline (GitHub Actions for build and deploy)
9. Testing (unit, integration, e2e)

---

*Plan generated 2025-12-28. Ready for `/sp.tasks` to generate implementation tasks.*
