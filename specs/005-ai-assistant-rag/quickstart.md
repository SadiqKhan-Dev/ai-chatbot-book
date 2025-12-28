# Quickstart Guide: AI Assistant RAG System

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- Qdrant Cloud account (or local Qdrant)
- Git

## Environment Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-org/ai-book.git
cd ai-book

# Switch to feature branch
git checkout 005-ai-assistant-rag
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=sk-...
# QDRANT_URL=https://...
# QDRANT_API_KEY=...
```

### 3. Frontend Setup (Docusaurus)

```bash
# Already in ai-book directory
cd ai-book

# Install Docusaurus dependencies (if not already)
npm install

# Install AI Assistant UI dependencies
cd src/theme/AIAssistant
npm install
```

### 4. Qdrant Setup

```bash
# Option A: Qdrant Cloud (recommended for production)
# 1. Create account at https://cloud.qdrant.io
# 2. Create new cluster
# 3. Copy API key and cluster URL to .env

# Option B: Local Qdrant (for development)
docker run -p 6333:6333 qdrant/qdrant
# Set QDRANT_URL=http://localhost:6333 in .env
```

## Running Locally

### 1. Start Qdrant (if local)

```bash
docker run -d --name qdrant-dev -p 6333:6333 qdrant/qdrant
```

### 2. Start the Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Index Book Content

```bash
cd backend
python -m scripts.index_content --path ../docs --batch-size 10
```

This will:
- Parse all Markdown files in the docs directory
- Split into semantic chunks
- Generate embeddings using OpenAI
- Store in Qdrant

### 4. Start Docusaurus

```bash
cd ai-book
npm start
```

The site will be available at `http://localhost:3000`
The AI Assistant will appear as a floating button in the corner.

## Testing the Chat

### Using curl

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is a digital twin?",
    "context_chapter": "/docs/physical-ai-robotics-course"
  }'
```

### Expected Response

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

## Development Commands

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest --cov` | Run tests with coverage |
| `black src/` | Format Python code |
| `ruff check src/` | Lint Python code |
| `npm run build` | Build Docusaurus site |
| `npm run serve` | Serve built site locally |

## Deployment

### Backend (Render example)

```bash
# Create Render app from GitHub
# Build command: pip install -r requirements.txt
# Start command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
# Add environment variables in Render dashboard
```

### Qdrant

Use Qdrant Cloud for production - free tier supports up to 1GB vectors.

### Docusaurus

```bash
# Build and deploy to GitHub Pages
npm run build
# CI/CD handles the rest via GitHub Actions
```

## Troubleshooting

### "Connection refused" to backend

- Verify backend is running on port 8000
- Check CORS settings in `src/core/config.py`
- Ensure no firewall blocking localhost

### "No embeddings found"

- Run `python -m scripts.index_content` to populate Qdrant
- Check Qdrant is running and accessible
- Verify OpenAI API key is valid

### Chat not loading in Docusaurus

- Check browser console for errors
- Verify backend URL is configured in UI
- Ensure Docusaurus swizzle was applied correctly

### Slow responses

- First request is slow due to cold start
- Consider keeping backend warm in production
- Check OpenAI API rate limits
