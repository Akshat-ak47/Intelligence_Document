from backend.agents.base_agent import BaseAgent
from backend.utils.exceptions import ParsingError
from pathlib import Path
import fitz
import docx

class ParserAgent(BaseAgent):
    def run(self, file_path: str):
        p = Path(file_path)
        if not p.exists():
            raise ParsingError('file not found')
        if p.suffix.lower() == '.pdf':
            doc = fitz.open(str(p))
            texts = [page.get_text() for page in doc]
            return '\n\n'.join([t for t in texts if t.strip()])
        elif p.suffix.lower() in ('.docx', '.doc'):
            d = docx.Document(str(p))
            paras = [p.text for p in d.paragraphs if p.text.strip()]
            return '\n\n'.join(paras)
        else:
            try:
                return p.read_text(encoding='utf-8')
            except Exception:
                raise ParsingError('unsupported file type')
