import json
from pathlib import Path
from backend.config import DATA_DIR
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

def save_doc(doc_id: str, text: str):
    p = Path(DATA_DIR) / f"{doc_id}.json"
    p.write_text(json.dumps({'doc_id': doc_id, 'text': text}, ensure_ascii=False), encoding='utf-8')
    return str(p)

def load_doc(doc_id: str):
    p = Path(DATA_DIR) / f"{doc_id}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))

def list_docs():
    return [p.stem for p in Path(DATA_DIR).glob('*.json')]
