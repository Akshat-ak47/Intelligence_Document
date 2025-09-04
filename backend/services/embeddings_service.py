"""Embeddings + Vector store service. Uses LangChain OpenAIEmbeddings and FAISS when available.
Provides simple semantic search fallback if FAISS missing.
"""
from backend.config import EMBEDDING_MODEL, VECTOR_DIR
from backend.utils.logger import get_logger
logger = get_logger(__name__)

try:
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    import faiss
    FAISS_AVAILABLE = True
except Exception as e:
    FAISS_AVAILABLE = False
    try:
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import Chroma
        CHROMA_AVAILABLE = True
    except Exception:
        CHROMA_AVAILABLE = False

import os, pickle
os.makedirs(VECTOR_DIR, exist_ok=True)
INDEX_PATH = os.path.join(VECTOR_DIR, 'faiss_index.pkl')

class EmbeddingsService:
    def __init__(self):
        self.emb = None
        self.vs = None
        try:
            self.emb = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        except Exception as e:
            logger.warning('OpenAIEmbeddings init failed: %s', e)
            self.emb = None
        if FAISS_AVAILABLE:
            if os.path.exists(INDEX_PATH):
                try:
                    with open(INDEX_PATH, 'rb') as f:
                        self.vs = pickle.load(f)
                except Exception:
                    self.vs = None
        elif CHROMA_AVAILABLE:
            self.vs = None

    def add_documents(self, texts: list, metadatas=None):
        if not texts:
            return
        if not self.emb:
            logger.warning('Embeddings client not configured; skipping add_documents')
            return
        if FAISS_AVAILABLE:
            if self.vs is None:
                self.vs = FAISS.from_texts(texts, self.emb)
            else:
                self.vs.add_texts(texts)
            with open(INDEX_PATH, 'wb') as f:
                pickle.dump(self.vs, f)
            logger.info('Added %d documents to FAISS index', len(texts))
        elif CHROMA_AVAILABLE:
            self.vs = Chroma.from_texts(texts, self.emb)
            logger.info('Added docs to Chroma (no persistence configured)')
        else:
            if getattr(self, 'memory', None) is None:
                self.memory = []
            self.memory.extend(texts)
            logger.warning('No vector DB available; using naive fallback')

    def search(self, query: str, k=3):
        if FAISS_AVAILABLE and self.vs:
            docs = self.vs.similarity_search(query, k=k)
            return [d.page_content for d in docs]
        elif CHROMA_AVAILABLE and self.vs:
            docs = self.vs.similarity_search(query, k=k)
            return [d.page_content for d in docs]
        else:
            res = []
            for t in getattr(self, 'memory', []):
                if query.lower() in t.lower():
                    res.append(t)
                    if len(res) >= k:
                        break
            return res

embeddings_service = EmbeddingsService()
