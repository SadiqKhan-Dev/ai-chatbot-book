---
id: "002"
title: "AI Assistant RAG System"
stage: "plan"
date_iso: "2025-12-28"
model: "sonnet-4-5-20250929"
feature: "ai-assistant-rag"
branch: "005-ai-assistant-rag"
user: "Human User"
command: "/sp.plan --title \"AI Assistant RAG System\" --description \"Creating implementation plan\""
labels: ["ai", "rag", "fastapi", "qdrant", "openai"]
links: "null"
files_yaml: |
  - specs/005-ai-assistant-rag/plan.md
  - specs/005-ai-assistant-rag/data-model.md
  - specs/005-ai-assistant-rag/quickstart.md
  - specs/005-ai-assistant-rag/contracts/openapi.yaml
tests_yaml: "null"
---

# PROMPT_TEXT

/sp.plan --title "AI Assistant RAG System" --description "Creating implementation plan"

Index Docusaurus content into Qdrant using embeddings.
Build a FastAPI-based RAG backend using OpenAI Agents/ChatKit SDKs.
Embed the AI agent UI into the Docusaurus site.
Deploy backend services and publish the book to GitHub Pages.

# RESPONSE_TEXT

Created implementation plan for AI Assistant RAG System. The plan defines a FastAPI backend with Qdrant vector storage and a React chat widget embedded in Docusaurus. Key technical decisions include using OpenAI Agents SDK with LangChain for RAG, text-embedding-3-small for embeddings, semantic chunking with 512-token chunks, and deployment to Render/Fly.io with Qdrant Cloud.

**Phase 0 Research Completed:**
- OpenAI Agents SDK + LangChain chosen over ChatKit
- Semantic chunking strategy for Markdown content
- Docusaurus Layout swizzle for chat widget
- Render/Fly.io for backend hosting
- text-embedding-3-small for cost/performance balance

**Phase 1 Artifacts Created:**
- plan.md - Full implementation plan with architecture
- data-model.md - Qdrant collections and Pydantic models
- quickstart.md - Setup and development guide
- contracts/openapi.yaml - API specification

Ready for `/sp.tasks` to generate implementation tasks.

---

**Architectural Decisions Documented:**

1. **SDK Selection**: OpenAI Agents SDK with LangChain for RAG implementation
2. **Chunking Strategy**: Semantic chunking with 512-token chunks and 50-token overlap
3. **Embedding Model**: text-embedding-3-small (cost-effective, 1536 dimensions)
4. **Deployment**: Render/Fly.io for backend, Qdrant Cloud for vectors
5. **Docusaurus Integration**: Layout swizzle with floating chat widget

---

**Next Step**: Run `/sp.tasks` to generate detailed implementation tasks.
