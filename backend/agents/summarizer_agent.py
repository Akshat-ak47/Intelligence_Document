from backend.agents.base_agent import BaseAgent
from backend.services.llm_service import chat_with_model
from backend.utils.langsmith_stub import log_agent_event

class SummarizerAgent(BaseAgent):
    def run(self, doc_id: str, text: str):
        prompt = (
            "You are an expert summarizer. Produce:\n"
            "1) Executive summary (3-5 sentences)\n"
            "2) 6-10 bullet points of key facts\n"
            "3) If sections exist, a short section-wise summary.\n\n"
            "Document:\n" + text[:30000]
        )
        out = chat_with_model('You are a helpful summarizer.', prompt, max_tokens=800)
        log_agent_event('summarizer', {'doc_id': doc_id}, {'summary_len': len(out)})
        return out
