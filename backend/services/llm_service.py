"""Simple LLM wrapper using OpenAI python package for chat/completion. We also provide a small helper to call LLMs.
"""
import openai
from backend.config import OPENAI_API_KEY, MODEL_NAME
from backend.utils.logger import get_logger
logger = get_logger(__name__)
openai.api_key = OPENAI_API_KEY


def chat_with_model(system: str, user_prompt: str, max_tokens=512, temperature=0.2):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_prompt}
    ]
    resp = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp['choices'][0]['message']['content'].strip()
