import streamlit as st
import os
import requests

API = os.getenv('API_URL', 'http://localhost:8000')

st.set_page_config(page_title='Doc Intelligence', layout='wide')
st.title('Intelligent Document Summarization & Q&A (AutoGen + LangChain + MCP)')

def safe_json_response(r):
    """Safely handle JSON or fallback to raw text"""
    try:
        return r.json()
    except Exception:
        return {"error": "Non-JSON response", "raw": r.text, "status": r.status_code}

st.sidebar.header('Upload')
uploaded = st.sidebar.file_uploader('Upload PDF/DOCX/TXT', type=['pdf','docx','txt'])
if uploaded:
    if st.sidebar.button('Upload & Process'):
        files = {'file': (uploaded.name, uploaded.getvalue())}
        with st.spinner('Uploading & running pipeline...'):
            r = requests.post(f"{API}/ingest/upload/", files=files)
        resp = safe_json_response(r)
        if r.status_code == 200:
            st.success('Processed')
            st.json(resp.get('result', resp))
        else:
            st.error("Backend error")
            st.code(resp)

st.sidebar.header('Docs')
if st.sidebar.button('List docs'):
    r = requests.get(f"{API}/list_Docs")   # instead of /doc
    resp = safe_json_response(r)
    if r.status_code == 200:
        st.write(resp)
    else:
        st.error("Backend error")
        st.code(resp)

st.header('Q&A')
doc_id = st.text_input('Doc ID (filename without extension)')
query = st.text_input('Question')
if st.button('Ask'):
    if not doc_id or not query:
        st.error('Provide doc id and a question')
    else:
        r = requests.post(f"{API}/qa/", data={'doc_id': doc_id, 'query': query})
        resp = safe_json_response(r)
        if r.status_code == 200:
            st.json(resp)
        else:
            st.error("Backend error")
            st.code(resp)

st.header('External Search (MCP Search Server)')
q = st.text_input('Query for external search')
if st.button('Search Web'):
    if q:
        r = requests.get(f"{API}/search-external/", params={'q': q})
        resp = safe_json_response(r)
        if r.status_code == 200:
            st.json(resp)
        else:
            st.error("Backend error")
            st.code(resp)
