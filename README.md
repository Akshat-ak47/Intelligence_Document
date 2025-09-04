# Intelligent Document Summarization & Q&A Platform (AutoGen + LangChain + MCP + Embeddings)

This project is a working starter that integrates:
- **AutoGen** (multi-agent orchestration via `autogen-agentchat`)
- **LangChain** embeddings with FAISS (semantic retrieval)
- **MCP** servers for FileOps and Search (FastAPI-based)
- **FastAPI** backend for orchestration and endpoints
- **Streamlit** UI for upload, review, Q&A

## Quick start (recommended)
1. Create and activate virtualenv (Python 3.10+):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in values (OPENAI_API_KEY required):
   ```bash
   cp .env.example .env
   ```

4. Start MCP servers (in separate terminals):
   ```bash
   python -m uvicorn mcp.servers.file_server:app --reload --port 9000
   python -m uvicorn mcp.servers.search_server:app --reload --port 9001
   ```

5. Start backend API:
   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```

6. Start Streamlit UI:
   ```bash
   python -m streamlit run ui/app.py --server.port 8501
   ```

Open http://localhost:8501 to use the UI.

## Notes
- The code contains fallbacks when optional dependencies (faiss, autogen) are missing; it will still run but with reduced features.
- For production: replace file-based storage with durable DB, secure API keys, and use a proper vector DB like Pinecone/Weaviate/Chroma.
