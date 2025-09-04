from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from backend.utils.logger import get_logger
from backend.services.mcp_client import mcp_client
from backend.storage import save_doc, load_doc, list_docs
from backend.agents.orchestrator import orchestrator
import os
from pathlib import Path

logger = get_logger(__name__)
app = FastAPI(title='Doc Intelligence Platform')

@app.post('/ingest/upload/')
async def ingest_upload(file: UploadFile = File(...)):
    try:
        data = await file.read()
        # upload to MCP File server
        mcp_client.upload_file(file.filename, data)
        # read back for parsing
        file_bytes = mcp_client.read_file(file.filename)
        local_path = os.path.join('tmp_uploads', file.filename)
        os.makedirs('tmp_uploads', exist_ok=True)
        with open(local_path, 'wb') as f:
            if isinstance(file_bytes, str):
                f.write(file_bytes.encode('utf-8'))
            else:
                f.write(file_bytes)
        result = orchestrator.run_pipeline(local_path)
        save_doc(result['doc_id'], result['text'])
        return {'status': 'ok', 'result': result}
    except Exception as e:
        logger.exception('ingest failed')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/docs')
async def docs_list():
    return {'docs': list_docs()}

@app.get('/doc/{doc_id}')
async def get_doc(doc_id: str):
    doc = load_doc(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail='not found')
    return doc

@app.post('/qa/')
async def qa(doc_id: str = Form(...), query: str = Form(...)):
    doc = load_doc(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail='doc not found')
    res = orchestrator.qa.run(doc_id, query, doc.get('text'))
    return res

@app.get('/search-external/')
async def external_search(q: str):
    return mcp_client.search(q)
