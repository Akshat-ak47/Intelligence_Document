#!/bin/bash
# Start MCP servers, backend and UI in separate terminals or use tmux
echo "Start MCP File server on 9000"
uvicorn mcp.servers.file_server:app --reload --port 9000 &
sleep 1
echo "Start MCP Search server on 9001"
uvicorn mcp.servers.search_server:app --reload --port 9001 &
sleep 1
echo "Start backend on 8000"
uvicorn backend.main:app --reload --port 8000 &
sleep 1
echo "Start Streamlit UI on 8501"
streamlit run ui/app.py --server.port 8501
