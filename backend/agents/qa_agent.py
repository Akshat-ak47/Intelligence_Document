from backend.agents.base_agent import BaseAgent
from backend.services.llm_service import chat_with_model
from backend.services.embeddings_service import embeddings_service
from backend.utils.langsmith_stub import log_agent_event

class QnAAgent(BaseAgent):
    def run(self, doc_id: str, query: str, doc_text: str = None):
        contexts = embeddings_service.search(query, k=3)
        if contexts:
            context = "\n\n".join(contexts)
            prompt = f"Use the following context to answer precisely. If answer is not contained, say 'I don't know'.\n\nCONTEXT:\n{context}\n\nQuestion: {query}\nAnswer:"
            ans = chat_with_model('Assistant for document Q&A', prompt, max_tokens=400)
            log_agent_event('qa_agent', {'doc_id': doc_id, 'query': query}, {'found_contexts': len(contexts)})
            return {'answer': ans, 'source': 'embeddings'}
        if doc_text and query.lower() in doc_text.lower():
            idx = doc_text.lower().find(query.lower())
            start = max(0, idx-200)
            end = min(len(doc_text), idx+200)
            snippet = doc_text[start:end]
            prompt = f"Use the snippet to answer. Snippet:\n{snippet}\nQuestion: {query}\nAnswer:"
            ans = chat_with_model('Assistant fallback', prompt, temperature=0.0)
            return {'answer': ans, 'source': 'document_snippet'}
        return {'answer': "I don't know based on the provided documents.", 'source': 'none'}
