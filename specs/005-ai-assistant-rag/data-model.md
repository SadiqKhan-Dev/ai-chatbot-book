# Data Model: AI Assistant RAG System

## Overview

This document describes the data models used by the AI Assistant RAG system, including entities for the vector database, chat sessions, and user interactions.

## Vector Database Schema (Qdrant)

### Collection: `book_chunks`

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier for the chunk |
| `vector` | array[float] | 1536-dimensional embedding |
| `payload.content` | string | The actual text content of the chunk |
| `payload.chapter_path` | string | Docusaurus URL path (e.g., `/docs/module-1/intro`) |
| `payload.chapter_title` | string | Human-readable chapter title |
| `payload.section_title` | string | Section heading within chapter |
| `payload.file_path` | string | Source file path |
| `payload.frontmatter` | object | Metadata from Markdown frontmatter |
| `payload.word_count` | int | Number of words in chunk |
| `payload.token_count` | int | Estimated token count |

### Collection: `conversations`

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique conversation identifier |
| `vector` | N/A | No embedding (metadata only) |
| `payload.user_id` | string | Anonymous session ID |
| `payload.created_at` | timestamp | Creation time |
| `payload.updated_at` | timestamp | Last activity time |
| `payload.title` | string | Generated title from first query |

### Collection: `messages`

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique message identifier |
| `vector` | N/A | No embedding (metadata only) |
| `payload.conversation_id` | UUID | Parent conversation |
| `payload.role` | enum | `user`, `assistant`, `system` |
| `payload.content` | string | Message text |
| `payload.citations` | array[object] | Source references |
| `payload.created_at` | timestamp | Message timestamp |

## API Data Models (Pydantic)

### ChatRequest

```python
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    selected_text: Optional[str] = Field(None, max_length=1000)
    conversation_id: Optional[str] = None
    context_chapter: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is a digital twin?",
                "selected_text": None,
                "conversation_id": None,
                "context_chapter": "/docs/digital-twin"
            }
        }
```

### ChatResponse

```python
class ChatResponse(BaseModel):
    response: str = Field(..., description="AI-generated answer")
    citations: List[Citation] = Field(default_factory=list)
    conversation_id: str = Field(..., description="Conversation identifier for follow-ups")

class Citation(BaseModel):
    chunk_id: str
    chapter_path: str
    title: str
    relevance_score: float = Field(..., ge=0, le=1)
    excerpt: Optional[str] = None
```

### ConversationResponse

```python
class ConversationResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    title: str
    message_count: int
```

### MessageResponse

```python
class MessageResponse(BaseModel):
    id: str
    role: str  # "user" | "assistant"
    content: str
    citations: List[Citation] = Field(default_factory=list)
    created_at: datetime
```

### Indexing Models

```python
class IndexStatus(BaseModel):
    status: str  # "idle" | "indexing" | "completed" | "failed"
    total_chunks: int
    indexed_chunks: int
    last_indexed_at: Optional[datetime]
    error: Optional[str] = None

class ReindexRequest(BaseModel):
    force: bool = False  # True to reindex even if unchanged
```

## Session Management

### Session Data (Redis or local storage)

```typescript
interface ChatSession {
  sessionId: string;
  conversations: {
    id: string;
    lastMessage: string;
    timestamp: Date;
  }[];
  preferences: {
    theme: 'light' | 'dark' | 'system';
    showCitations: boolean;
  };
}
```

## Content Chunking Rules

### Chunk Strategy

1. **Maximum chunk size**: 512 tokens
2. **Overlap**: 50 tokens between chunks
3. **Split boundaries**:
   - H1, H2, H3 headers
   - Code blocks (kept intact with preceding explanation)
   - Empty lines (double newline)

### Metadata Extraction

```python
def extract_metadata(markdown_content: str, file_path: str) -> dict:
    frontmatter = extract_frontmatter(markdown_content)  # YAML between ---
    title = frontmatter.get('title', extract_first_h1(markdown_content))
    chapter_path = file_path_to_url(file_path)  # docs/ -> /docs/
    section = extract_current_section(markdown_content)
    return {
        'title': title,
        'chapter_path': chapter_path,
        'section_title': section,
        'file_path': file_path,
        'frontmatter': frontmatter
    }
```
