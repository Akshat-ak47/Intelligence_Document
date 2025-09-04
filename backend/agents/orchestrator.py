"""Orchestrator: uses AutoGen when available, else runs a simple sequential pipeline."""
from backend.utils.logger import get_logger
logger = get_logger(__name__)

try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    AUTOGEN_AVAILABLE = True
except Exception:
    AUTOGEN_AVAILABLE = False

from backend.agents.parser_agent import ParserAgent
from backend.agents.summarizer_agent import SummarizerAgent
from backend.agents.entity_agent import EntityAgent
from backend.agents.qa_agent import QnAAgent
from backend.agents.validator_agent import ValidatorAgent
from backend.services.embeddings_service import embeddings_service

class Orchestrator:
    def __init__(self):
        self.parser = ParserAgent()
        self.summarizer = SummarizerAgent()
        self.entity = EntityAgent()
        self.qa = QnAAgent()
        self.validator = ValidatorAgent()

    def run_pipeline(self, file_path: str):
        text = self.parser.run(file_path)
        doc_id = Path(file_path).stem if '/' in file_path or '\\' in file_path else file_path
        # summarize
        summary = self.summarizer.run(doc_id, text)
        # entities
        entities = self.entity.run(doc_id, text)
        # add embeddings
        try:
            embeddings_service.add_documents([text], metadatas=[{'doc_id': doc_id}])
        except Exception as e:
            logger.warning('embeddings add failed: %s', e)
        # validate
        validation = self.validator.run(doc_id, summary, entities)
        return {
            'doc_id': doc_id,
            'text': text,
            'summary': summary,
            'entities': entities,
            'validation': validation
        }

orchestrator = Orchestrator()
