from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploaded_docs')
DATA_DIR = os.getenv('DATA_DIR', 'data_store')
VECTOR_DIR = os.getenv('VECTOR_DIR', 'vector_db')
MCP_FILE_SERVER_URL = os.getenv('MCP_FILE_SERVER_URL', 'http://localhost:9000')
MCP_SEARCH_SERVER_URL = os.getenv('MCP_SEARCH_SERVER_URL', 'http://localhost:9001')
